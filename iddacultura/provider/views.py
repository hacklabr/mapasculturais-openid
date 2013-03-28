# -*- coding: utf-8 -*-

"""
This module implements an example server for the OpenID library.  Some
functionality has been omitted intentionally; this code is intended to
be instructive on the use of this library.  This server does not
perform actual user authentication and serves up only one OpenID URL,
with the exception of IDP-generated identifiers.

Some code conventions used here:

* 'request' is a Django request object.

* 'openid_request' is an OpenID library request object.

* 'openid_response' is an OpenID library response
"""

import cgi
import urllib

from iddacultura.provider import util
from iddacultura.provider.util import get_view_url
from iddacultura.models import TrustedRoot 

from profiles.views import profile_detail

from django import http
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import redirect_to_login

from openid.server.server import Server, ProtocolError, EncodingError
from openid.server.trustroot import verifyReturnTo
from openid.yadis.discover import DiscoveryFailure
from openid.consumer.discover import OPENID_IDP_2_0_TYPE, OPENID_2_0_TYPE
from openid.extensions import sreg
from openid.extensions import pape
from openid.fetchers import HTTPFetchingError

def get_openid_store():
    """
    Return an OpenID store object fit for the currently-chosen
    database backend, if any.
    """
    return util.get_openid_store('/tmp/djopenid_s_store', 's_')

def get_server(request):
    """
    Get a Server object to perform OpenID authentication.
    """
    return Server(get_openid_store(), get_view_url(request, endpoint))

def set_request(request, openid_request):
    """
    Store the openid request information in the session.
    """
    if openid_request:
        request.session['openid_request'] = openid_request
    else:
        request.session['openid_request'] = None

def get_request(request):
    """
    Get an openid request from the session, if any.
    """
    return request.session.get('openid_request')

def op_xrds(request):
    """
    Respond to requests for the OpenID Provider XRDS document, which is used in
    IDP-driven identifier selection.
    """
    return util.render_xrds(
        request, [OPENID_IDP_2_0_TYPE, sreg.ns_uri], [get_view_url(request, endpoint)])

def user_xrds(request, username):
    """
    Respond to requests for a specific user identity XRDS Document
    """
    return util.render_xrds(
        request, [OPENID_2_0_TYPE, sreg.ns_uri], [get_view_url(request, endpoint)], username)

def trust_page(request):
    """
    Display the trust page template, which allows the user to decide
    whether to approve the OpenID verification.
    """
    return direct_to_template(
        request,
        'provider/trust.html',
        {'trust_handler_url':get_view_url(request, process_trust_result)})

@csrf_exempt
def endpoint(request):
    """
    Respond to low-level OpenID protocol messages.
    """
    s = get_server(request)

    query = util.normal_dict(request.GET or request.POST)

    # First, decode the incoming request into something the OpenID
    # library can use.
    try:
        openid_request = s.decodeRequest(query)
    except ProtocolError, why:
        # This means the incoming request was invalid.
        return direct_to_template(
            request,
            'provider/endpoint.html',
            {'error': str(why)})

    # If we did not get a request, display text indicating that this
    # is an endpoint.
    if openid_request is None:
        return direct_to_template(
            request,
            'provider/endpoint.html',
            {})

    # We got a request; if the mode is checkid_*, we will handle it by
    # getting feedback from the user or by checking the session.
    if openid_request.mode in ["checkid_immediate", "checkid_setup"]:
        if not request.user or request.user.is_authenticated() == False:
            #TODO: verificar porque o openid_request.encodeToURL() remove os parâmetros relacionados com a extensão SREG
            return redirect_to_login(request.get_full_path() + '?' + urllib.urlencode(query))
        
        user_identity = request.build_absolute_uri(request.user.get_profile().get_absolute_url())
        
        if not openid_request.identity == user_identity and not openid_request.idSelect():
            raise Exception, "User " + request.user.username + " is not the owner of " + openid_request.identity + " identity"
        
        return handle_check_id_request(request, openid_request)
    else:
        # We got some other kind of OpenID request, so we let the
        # server handle this.
        openid_response = s.handleRequest(openid_request)
        return display_response(request, openid_response)

def handle_check_id_request(request, openid_request):
    """
    Handle checkid_* requests.  Get input from the user to find out
    whether she trusts the RP involved.  Possibly, get intput about
    what Simple Registration information, if any, to send in the
    response.
    """
    
    id_url = get_view_url(request, profile_detail, {request.user.username})
    
    # If the request was an IDP-driven identifier selection request
    # (i.e., the IDP URL was entered at the RP), then return the
    # default identity URL for this server. In a full-featured
    # provider, there could be interaction with the user to determine
    # what URL should be sent.
    if not openid_request.idSelect():
        # Confirm that this server can actually vouch for that
        # identifier
        if id_url != openid_request.identity:
            # Return an error response
            error_response = ProtocolError(
                openid_request.message,
                "This server cannot verify the URL %r" %
                (openid_request.identity,))

            return display_response(request, error_response)

    if request.user.userprofile.trusted_url(openid_request.trust_root):
        openid_response = openid_request.answer(True, identity = id_url)
        return display_response(request, openid_response)

    if openid_request.immediate:
        # Always respond with 'cancel' to immediate mode requests
        # because we don't track information about a logged-in user.
        # If we did, then the answer would depend on whether that user
        # had trusted the request's trust root and whether the user is
        # even logged in.
        openid_response = openid_request.answer(False)
        return display_response(request, openid_response)
    else:
        # Store the incoming request object in the session so we can
        # get to it later.
        set_request(request, openid_request)
        return show_decide_page(request, openid_request)

def show_decide_page(request, openid_request):
    """
    Render a page to the user so a trust decision can be made.

    @type openid_request: openid.server.server.CheckIDRequest
    """
    trust_root = openid_request.trust_root
    return_to = openid_request.return_to

    try:
        # Stringify because template's ifequal can only compare to strings.
        trust_root_valid = verifyReturnTo(trust_root, return_to) \
                           and "Valid" or "Invalid"
    except DiscoveryFailure, err:
        trust_root_valid = "DISCOVERY_FAILED"
    except HTTPFetchingError, err:
        trust_root_valid = "Unreachable"

    pape_request = pape.Request.fromOpenIDRequest(openid_request)

    return direct_to_template(
        request,
        'provider/trust.html',
        {'trust_root': trust_root,
         'trust_handler_url':get_view_url(request, process_trust_result),
         'trust_root_valid': trust_root_valid,
         'pape_request': pape_request,
         })

@csrf_exempt
def process_trust_result(request):
    """
    Handle the result of a trust decision and respond to the RP
    accordingly.
    """
    # Get the request from the session so we can construct the
    # appropriate response.
    openid_request = get_request(request)

    # The identifier that this server can vouch for
    response_identity = get_view_url(request, profile_detail, {request.user.username})

    # If the decision was to allow the verification, respond
    # accordingly.
    allowed = 'allow' in request.POST

    # Generate a response with the appropriate answer.
    openid_response = openid_request.answer(allowed,
                                            identity=response_identity)

    if request.POST.has_key('remember') and request.POST['remember'] == 'yes':
        url = TrustedRoot.objects.get(url = openid_response.request.trust_root)
        request.user.userprofile.trusted_roots.add(url)

    # Send Simple Registration data in the response, if appropriate.
    if allowed:
        sreg_data = {
            'fullname': request.user.get_full_name(),
            'nickname': request.user.username,
            'email': request.user.email,
            'postcode': request.user.get_profile().cpf,
        }

        sreg_req = sreg.SRegRequest.fromOpenIDRequest(openid_request)
        sreg_resp = sreg.SRegResponse.extractResponse(sreg_req, sreg_data)
        openid_response.addExtension(sreg_resp)

        pape_response = pape.Response()
        pape_response.setAuthLevel(pape.LEVELS_NIST, 0)
        openid_response.addExtension(pape_response)

    return display_response(request, openid_response)

def display_response(request, openid_response):
    """
    Display an OpenID response.  Errors will be displayed directly to
    the user; successful responses and other protocol-level messages
    will be sent using the proper mechanism (i.e., direct response,
    redirection, etc.).
    """
    s = get_server(request)

    # Encode the response into something that is renderable.
    try:
        webresponse = s.encodeResponse(openid_response)
    except EncodingError, why:
        # If it couldn't be encoded, display an error.
        text = why.response.encodeToKVForm()
        return direct_to_template(
            request,
            'provider/endpoint.html',
            {'error': cgi.escape(text)})

    # Construct the appropriate django framework response.
    r = http.HttpResponse(webresponse.body)
    r.status_code = webresponse.code

    for header, value in webresponse.headers.iteritems():
        r[header] = value

    return r
config = {

    # This config file is used only in appengine.beecoss.com (Sample website)


    # Don't use values defined here
    'environment': "boilerplate",

    # application name
    'app_name': "Testing Boiler Plate",

    # contact page email settings
    'contact_sender': "ammj@oregonstate.edu",
    'contact_recipient': "ammj@oregonstate.edu",

    'send_mail_developer': False,

    # fellas' list
    'developers': (
        ('GAE Developer', 'ammj@oregonstate.edu'),
    ),

    # It is just an example to fill out this value
    #'google_analytics_code': "",

    # Password AES Encryption Parameters
    # aes_key must be only 16 (*AES-128*), 24 (*AES-192*), or 32 (*AES-256*) bytes (characters) long.
    # updated by ammj
    #'aes_key': "9c20576a4330bbe719b23ac8bf3bb8a1",
    #'salt': "RdbkETeF$<^>%%X^8|e[9td62`dobFL[V&F&**@`UP6vqjGL,>v+k@ma^zd6WdG0;H>o-SGG9ynk",
    'aes_key': "86c16b40beb9560ad615597247c1d496b1438cb2b353g95092eb906330676055",
    'salt': ":PenZ7#C<_(q!&eF,FmUf<^>D33CFVjp7CS7FC:9q!}UqszrS9Q6Hm#9W;PYn$>",

    # get your own consumer key and consumer secret by registering at https://dev.twitter.com/apps
    # callback url must be: http://[YOUR DOMAIN]/login/twitter/complete
    #'twitter_consumer_key': '',
    #'twitter_consumer_secret': '',

    #Facebook Login
    # get your own consumer key and consumer secret by registering at https://developers.facebook.com/apps
    #Very Important: set the site_url= your domain in the application settings in the facebook app settings page
    # callback url must be: http://[YOUR DOMAIN]/login/facebook/complete
    #'fb_api_key': '',
    #'fb_secret': '',

    #Linkedin Login
    #Get you own api key and secret from https://www.linkedin.com/secure/developer
    #'linkedin_api': '',
    #'linkedin_secret': '',

    # Github login
    # Register apps here: https://github.com/settings/applications/new
    #'github_server': '',
    #'github_redirect_uri': '',
    #'github_client_id': '',
    #'github_client_secret': '',

    # get your own recaptcha keys by registering at http://www.google.com/recaptcha/
    # updated by ammj
    'captcha_public_key': "6LdkvxwTAAAAANO7pPko0C7tUuS3_RffSigX74M_",
    'captcha_private_key': "6LdkvxwTAAAAAPVhpE32mzg8N-A_G5x0-PvFrwkU",

    # webapp2 sessions
    # updated by ammj
    'webapp2_extras.sessions': { 'secret_key': 'ammj#W1|(|=_>}m9BZEB#drBG| tN@0{@7+)gB:w:+9u3}nlrf8U?' },

    # webapp2 authentication
    'webapp2_extras.auth': { 'cookie_name': 'gae_session' },

    # ----> ADD MORE CONFIGURATION OPTIONS HERE <----

}
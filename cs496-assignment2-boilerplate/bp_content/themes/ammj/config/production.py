config = {
    'environment': "production",

    # application name
    'app_name': "Testing in Production",

    # contact page email settings
    'contact_sender': "ammj@oregonstate.edu",
    'contact_recipient': "ammj@oregonstate.edu",

    # Password AES Encryption Parameters
    # aes_key must be only 16 (*AES-128*), 24 (*AES-192*), or 32 (*AES-256*) bytes (characters) long.
    # 'aes_key': "12_24_32_BYTES_KEY_FOR_PASSWORDS",
    # 'salt': "_PUT_SALT_HERE_TO_SHA512_PASSWORDS_",
    'aes_key': "86c16b40beb9560ad615597247c1d49b",
    'salt': "thisismysaltforthistest",

    # get your own recaptcha keys by registering at http://www.google.com/recaptcha/
    'captcha_public_key': "6LdkvxwTAAAAANO7pPko0C7tUuS3_RffSigX74M_",
    'captcha_private_key': "6LdkvxwTAAAAAPVhpE32mzg8N-A_G5x0-PvFrwkU",

    # fellas' list
    'developers': (
        ('Jeannine Amm', 'ammj@oregonstate.edu'),
    ),

    # ----> ADD MORE CONFIGURATION OPTIONS HERE <----

} 

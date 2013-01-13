# -*- coding: utf-8 -*-
from users.forms import RegistrationFormFranchisee
import datetime, random, sha
from users.models import UserProfile, CreateCodes
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

class UserRegistration(object):
        
    def __init__(self, form):
        """
            Instantiating the `form` with ajax to process information
            :param form: Form object ajax.py
        """
        self._form = form
        
        
    def cleanData(self):
        """
            method or function responsible for cleaning objects oder
            `form` to be read by python, returns a JSON
        """
        # Clean Fields
        self._identification = self._form.cleaned_data['identification']
        self._email          = self._form.cleaned_data['email']
        self._passwordOne    = self._form.cleaned_data['passwordOne']
        self._passwordTwo    = self._form.cleaned_data['passwordTwo']
        self._franchiseeCode = self._form.cleaned_data['franchiseeCode']
        #JSON
        self._data = {
                'identification': self._identification,
                'email': self._email,
                'passwordOne':self._passwordOne,
                'passwordTwo':self._passwordTwo,
                'franchiseeCode':self._franchiseeCode 
            }
        
        return self._data
    
    
    def validDataFranchisee(self):
        """
            method or function which validates the following fields:
            :param franchisee: identification of the franchisee
            :param email: email the franchisee
            :param franchiseCode: franchisee referenced code that is available.
            
        """
        # verifying that the user does not exist
        self._validFranchisee = self._form.isValidFranchisee(self._identification)
        # verifying that the email does not exist
        self._validFranchiseeEmail = self._form.isValidFranchiseeEmail(self._email)
        # verifying that the user code does not exist or used
        self._validFranchiseeCode = self._form.isValidFranchiseeCode(self._franchiseeCode)
                
        return {'franchisee': self._validFranchisee, 'email': self._validFranchiseeEmail, 'franchiseeCode': self._validFranchiseeCode}
    
    
    def saveUser(self):
        """ Save the user """
        self._user = self._form.save(self._data)
        
    
    def activationKey(self):
        """
            This method or function is responsible for creating
            the activation code and expiration date
        """
        # Build the activation key for their account
        initial  = sha.new(str(random.random())).hexdigest()[:5]
        self._activationKey  = sha.new(initial+self._identification).hexdigest()
        self._keyExpires     = datetime.datetime.today() + datetime.timedelta(2)
        self._dataActivation = {'activatioCode':self._activationKey, 'keyExpires':self._keyExpires}
    
    
    def newUserProfile(self):
        """
            This method or function creates the new user along with the profile
            that is initially disabled, returns the number of the Franchisee
            which referenced where applicable.
        """
        # when the user registers with Code
        if self._validFranchiseeCode['flag'] == True:
            
            user = UserProfile.objects.get(identification=self._validFranchiseeCode['id'])
            
            newProfile = UserProfile(
                        identification=self._user, activationKey=self._activationKey,
                        keyExpires=self._keyExpires, refFranchiseeCode=self._franchiseeCode,
                        refFranchisee=user)
            #update Code in list for user; assigning values ​​necessary to use the code and date of use
            CreateCodes.objects.filter(code=self._data['franchiseeCode']).update(useFlagCode=True, dateUseFlag=datetime.datetime.now())
            
        # when the user is logged without Code
        else:
            newProfile = UserProfile(
                        identification=self._user, activationKey=self._activationKey,
                        keyExpires=self._keyExpires, refFranchiseeCode=None)
        
        # Save the profile
        newProfile.save()
        
        
    def send_mails(self, mail):
        """
            This method or function is responsible for sending the email
            to activate as the case of Franchisee or Franchisee Referenced  
        """
        subject = 'Confirmación de Registro en elevatusventas.com'
        # Send an email with the confirmation link
        if self._validFranchiseeCode['flag'] == True:
            #body = "<!DOCTYPE html><html><head><html lang='es'><link href='netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/css/bootstrap-combined.min.css' rel='stylesheet'><script src='netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/js/bootstrap.min.js'></script></head><body><h1>Hola Franquiciado</h1>, %s, and thanks for signing up for an \n elevatusventas.com account!\n\nTo activate your account, click this link within 48 \hours:\n\nhttp://example.com/accounts/confirm/%s <span class='label label-info'>alejo8591@gmail.com</span></body></html>"% (
             #           self._identification,
             #           self._activationKey)
             body = """
                        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                        <html>
                            <head>
                                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                                
                                <!-- Facebook sharing information tags -->
                                <meta property="og:title" content="*|MC:SUBJECT|*" />
                                
                                <title>*|MC:SUBJECT|*</title>
                                        <style type="text/css">
                                                /* Client-specific Styles */
                                                #outlook a{padding:0;} /* Force Outlook to provide a "view in browser" button. */
                                                body{width:100% !important;} .ReadMsgBody{width:100%;} .ExternalClass{width:100%;} /* Force Hotmail to display emails at full width */
                                                body{-webkit-text-size-adjust:none;} /* Prevent Webkit platforms from changing default text sizes. */
                        
                                                /* Reset Styles */
                                                body{margin:0; padding:0;}
                                                img{border:0; height:auto; line-height:100%; outline:none; text-decoration:none;}
                                                table td{border-collapse:collapse;}
                                                #backgroundTable{height:100% !important; margin:0; padding:0; width:100% !important;}
                        
                                                /* Template Styles */
                        
                                                /* /\/\/\/\/\/\/\/\/\/\ STANDARD STYLING: COMMON PAGE ELEMENTS /\/\/\/\/\/\/\/\/\/\ */
                        
                                                /**
                                                * @tab Page
                                                * @section background color
                                                * @tip Set the background color for your email. You may want to choose one that matches your company's branding.
                                                * @theme page
                                                */
                                                body, #backgroundTable{
                                                        /*@editable*/ background-color:#FAFAFA;
                                                }
                        
                                                /**
                                                * @tab Page
                                                * @section email border
                                                * @tip Set the border for your email.
                                                */
                                                #templateContainer{
                                                        /*@editable*/ border: 1px solid #DDDDDD;
                                                }
                        
                                                /**
                                                * @tab Page
                                                * @section heading 1
                                                * @tip Set the styling for all first-level headings in your emails. These should be the largest of your headings.
                                                * @style heading 1
                                                */
                                                h1, .h1{
                                                        /*@editable*/ color:#202020;
                                                        display:block;
                                                        /*@editable*/ font-family:Arial;
                                                        /*@editable*/ font-size:34px;
                                                        /*@editable*/ font-weight:bold;
                                                        /*@editable*/ line-height:100%;
                                                        margin-top:0;
                                                        margin-right:0;
                                                        margin-bottom:10px;
                                                        margin-left:0;
                                                        /*@editable*/ text-align:left;
                                                }
                        
                                                /**
                                                * @tab Page
                                                * @section heading 2
                                                * @tip Set the styling for all second-level headings in your emails.
                                                * @style heading 2
                                                */
                                                h2, .h2{
                                                        /*@editable*/ color:#202020;
                                                        display:block;
                                                        /*@editable*/ font-family:Arial;
                                                        /*@editable*/ font-size:30px;
                                                        /*@editable*/ font-weight:bold;
                                                        /*@editable*/ line-height:100%;
                                                        margin-top:0;
                                                        margin-right:0;
                                                        margin-bottom:10px;
                                                        margin-left:0;
                                                        /*@editable*/ text-align:left;
                                                }
                        
                                                /**
                                                * @tab Page
                                                * @section heading 3
                                                * @tip Set the styling for all third-level headings in your emails.
                                                * @style heading 3
                                                */
                                                h3, .h3{
                                                        /*@editable*/ color:#202020;
                                                        display:block;
                                                        /*@editable*/ font-family:Arial;
                                                        /*@editable*/ font-size:26px;
                                                        /*@editable*/ font-weight:bold;
                                                        /*@editable*/ line-height:100%;
                                                        margin-top:0;
                                                        margin-right:0;
                                                        margin-bottom:10px;
                                                        margin-left:0;
                                                        /*@editable*/ text-align:left;
                                                }
                        
                                                /**
                                                * @tab Page
                                                * @section heading 4
                                                * @tip Set the styling for all fourth-level headings in your emails. These should be the smallest of your headings.
                                                * @style heading 4
                                                */
                                                h4, .h4{
                                                        /*@editable*/ color:#202020;
                                                        display:block;
                                                        /*@editable*/ font-family:Arial;
                                                        /*@editable*/ font-size:22px;
                                                        /*@editable*/ font-weight:bold;
                                                        /*@editable*/ line-height:100%;
                                                        margin-top:0;
                                                        margin-right:0;
                                                        margin-bottom:10px;
                                                        margin-left:0;
                                                        /*@editable*/ text-align:left;
                                                }
                        
                                                /* /\/\/\/\/\/\/\/\/\/\ STANDARD STYLING: HEADER /\/\/\/\/\/\/\/\/\/\ */
                        
                                                /**
                                                * @tab Header
                                                * @section header style
                                                * @tip Set the background color and border for your email's header area.
                                                * @theme header
                                                */
                                                #templateHeader{
                                                        /*@editable*/ background-color:#FFFFFF;
                                                        /*@editable*/ border-bottom:0;
                                                }
                        
                                                /**
                                                * @tab Header
                                                * @section header text
                                                * @tip Set the styling for your email's header text. Choose a size and color that is easy to read.
                                                */
                                                .headerContent{
                                                        /*@editable*/ color:#202020;
                                                        /*@editable*/ font-family:Arial;
                                                        /*@editable*/ font-size:34px;
                                                        /*@editable*/ font-weight:bold;
                                                        /*@editable*/ line-height:100%;
                                                        /*@editable*/ padding:0;
                                                        /*@editable*/ text-align:center;
                                                        /*@editable*/ vertical-align:middle;
                                                }
                        
                                                /**
                                                * @tab Header
                                                * @section header link
                                                * @tip Set the styling for your email's header links. Choose a color that helps them stand out from your text.
                                                */
                                                .headerContent a:link, .headerContent a:visited, /* Yahoo! Mail Override */ .headerContent a .yshortcuts /* Yahoo! Mail Override */{
                                                        /*@editable*/ color:#336699;
                                                        /*@editable*/ font-weight:normal;
                                                        /*@editable*/ text-decoration:underline;
                                                }
                        
                                                #headerImage{
                                                        height:auto;
                                                        max-width:600px !important;
                                                }
                        
                                                /* /\/\/\/\/\/\/\/\/\/\ STANDARD STYLING: MAIN BODY /\/\/\/\/\/\/\/\/\/\ */
                        
                                                /**
                                                * @tab Body
                                                * @section body style
                                                * @tip Set the background color for your email's body area.
                                                */
                                                #templateContainer, .bodyContent{
                                                        /*@editable*/ background-color:#FFFFFF;
                                                }
                        
                                                /**
                                                * @tab Body
                                                * @section body text
                                                * @tip Set the styling for your email's main content text. Choose a size and color that is easy to read.
                                                * @theme main
                                                */
                                                .bodyContent div{
                                                        /*@editable*/ color:#505050;
                                                        /*@editable*/ font-family:Arial;
                                                        /*@editable*/ font-size:14px;
                                                        /*@editable*/ line-height:150%;
                                                        /*@editable*/ text-align:left;
                                                }
                        
                                                /**
                                                * @tab Body
                                                * @section body link
                                                * @tip Set the styling for your email's main content links. Choose a color that helps them stand out from your text.
                                                */
                                                .bodyContent div a:link, .bodyContent div a:visited, /* Yahoo! Mail Override */ .bodyContent div a .yshortcuts /* Yahoo! Mail Override */{
                                                        /*@editable*/ color:#336699;
                                                        /*@editable*/ font-weight:normal;
                                                        /*@editable*/ text-decoration:underline;
                                                }
                        
                                                /**
                                                * @tab Body
                                                * @section button style
                                                * @tip Set the styling for your email's button. Choose a style that draws attention.
                                                */
                                                .templateButton{
                                                        -moz-border-radius:3px;
                                                        -webkit-border-radius:3px;
                                                        /*@editable*/ background-color:#336699;
                                                        /*@editable*/ border:0;
                                                        border-collapse:separate !important;
                                                        border-radius:3px;
                                                }
                        
                                                /**
                                                * @tab Body
                                                * @section button style
                                                * @tip Set the styling for your email's button. Choose a style that draws attention.
                                                */
                                                .templateButton, .templateButton a:link, .templateButton a:visited, /* Yahoo! Mail Override */ .templateButton a .yshortcuts /* Yahoo! Mail Override */{
                                                        /*@editable*/ color:#FFFFFF;
                                                        /*@editable*/ font-family:Arial;
                                                        /*@editable*/ font-size:15px;
                                                        /*@editable*/ font-weight:bold;
                                                        /*@editable*/ letter-spacing:-.5px;
                                                        /*@editable*/ line-height:100%;
                                                        text-align:center;
                                                        text-decoration:none;
                                                }
                        
                                                .bodyContent img{
                                                        display:inline;
                                                        height:auto;
                                                }
                        
                                                /* /\/\/\/\/\/\/\/\/\/\ STANDARD STYLING: FOOTER /\/\/\/\/\/\/\/\/\/\ */
                        
                                                /**
                                                * @tab Footer
                                                * @section footer style
                                                * @tip Set the background color and top border for your email's footer area.
                                                * @theme footer
                                                */
                                                #templateFooter{
                                                        /*@editable*/ background-color:#FFFFFF;
                                                        /*@editable*/ border-top:0;
                                                }
                        
                                                /**
                                                * @tab Footer
                                                * @section footer text
                                                * @tip Set the styling for your email's footer text. Choose a size and color that is easy to read.
                                                * @theme footer
                                                */
                                                .footerContent div{
                                                        /*@editable*/ color:#707070;
                                                        /*@editable*/ font-family:Arial;
                                                        /*@editable*/ font-size:12px;
                                                        /*@editable*/ line-height:125%;
                                                        /*@editable*/ text-align:center;
                                                }
                        
                                                /**
                                                * @tab Footer
                                                * @section footer link
                                                * @tip Set the styling for your email's footer links. Choose a color that helps them stand out from your text.
                                                */
                                                .footerContent div a:link, .footerContent div a:visited, /* Yahoo! Mail Override */ .footerContent div a .yshortcuts /* Yahoo! Mail Override */{
                                                        /*@editable*/ color:#336699;
                                                        /*@editable*/ font-weight:normal;
                                                        /*@editable*/ text-decoration:underline;
                                                }
                        
                                                .footerContent img{
                                                        display:inline;
                                                }
                        
                                                /**
                                                * @tab Footer
                                                * @section utility bar style
                                                * @tip Set the background color and border for your email's footer utility bar.
                                                * @theme footer
                                                */
                                                #utility{
                                                        /*@editable*/ background-color:#FFFFFF;
                                                        /*@editable*/ border:0;
                                                }
                        
                                                /**
                                                * @tab Footer
                                                * @section utility bar style
                                                * @tip Set the background color and border for your email's footer utility bar.
                                                */
                                                #utility div{
                                                        /*@editable*/ text-align:center;
                                                }
                        
                                                #monkeyRewards img{
                                                        max-width:190px;
                                                }
                                        </style>
                                </head>
                            <body leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0">
                                <center>
                                        <table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="backgroundTable">
                                        <tr>
                                                <td align="center" valign="top" style="padding-top:20px;">
                                                <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateContainer">
                                                        <tr>
                                                        <td align="center" valign="top">
                                                            <!-- // Begin Template Header \\ -->
                                                                <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateHeader">
                                                                <tr>
                                                                    <td class="headerContent">
                                                                    
                                                                        <!-- // Begin Module: Standard Header Image \\ -->
                                                                        <img src="http://gallery.mailchimp.com/653153ae841fd11de66ad181a/images/placeholder_600.gif" style="max-width:600px;" id="headerImage campaign-icon" mc:label="header_image" mc:edit="header_image" mc:allowdesigner mc:allowtext />
                                                                        <!-- // End Module: Standard Header Image \\ -->
                                                                    
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <!-- // End Template Header \\ -->
                                                        </td>
                                                    </tr>
                                                        <tr>
                                                        <td align="center" valign="top">
                                                            <!-- // Begin Template Body \\ -->
                                                                <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateBody">
                                                                <tr>
                                                                    <td valign="top">
                                                        
                                                                        <!-- // Begin Module: Standard Content \\ -->
                                                                        <table border="0" cellpadding="20" cellspacing="0" width="100%">
                                                                            <tr>
                                                                                <td valign="top" class="bodyContent">
                                                                                    <div mc:edit="std_content00">
                                                                                        <h1 class="h1">Heading 1</h1>
                                                                                        <h2 class="h2">Heading 2</h2>
                                                                                        <h3 class="h3">Heading 3</h3>
                                                                                        <h4 class="h4">Heading 4</h4>
                                                                                        <strong>Getting started:</strong> Transactional emails serve a defined and simple purpose. They differ from traditional mass-emails because they're generally sent on a user-by-user basis, instead of large list of users, and are generally used to deliver purchase receipts, account updates, security notifications, and more.
                                                                                        <br />
                                                                                        <br />
                                                                                        Where <a href="http://www.mailchimp.com/" target="_blank">MailChimp</a> can be used to send newsletters to several subscribers in one large blast, <a href="http://www.mandrill.com/" target="_blank">Mandrill</a> is specifically positioned to send transactional emails, and offers relevant tracking and metrics that isn't necessarily available through a traditional email platform.
                                                                                    </div>
                                                                                                                                        </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="center" valign="top" style="padding-top:0;">
                                                                                        <table border="0" cellpadding="15" cellspacing="0" class="templateButton">
                                                                                        <tr>
                                                                                                <td valign="middle" class="templateButtonContent">
                                                                                                <div mc:edit="std_content01">
                                                                                                        <a href="http://www.mandrill.com/" target="_blank">See What Mandrill Can Do</a>
                                                                                                </div>
                                                                                            </td>
                                                                                        </tr>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </table>
                                                                        <!-- // End Module: Standard Content \\ -->
                                                                        
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <!-- // End Template Body \\ -->
                                                        </td>
                                                    </tr>
                                                        <tr>
                                                        <td align="center" valign="top">
                                                            <!-- // Begin Template Footer \\ -->
                                                                <table border="0" cellpadding="10" cellspacing="0" width="600" id="templateFooter">
                                                                <tr>
                                                                        <td valign="top" class="footerContent">
                                                                    
                                                                        <!-- // Begin Module: Transactional Footer \\ -->
                                                                        <table border="0" cellpadding="10" cellspacing="0" width="100%">
                                                                            <tr>
                                                                                <td valign="top">
                                                                                    <div mc:edit="std_footer">
                                                                                                                                                        <em>Copyright &copy; *|CURRENT_YEAR|* *|LIST:COMPANY|*, All rights reserved.</em>
                                                                                                                                                        <br />
                                                                                                                                                        *|IFNOT:ARCHIVE_PAGE|* *|LIST:DESCRIPTION|*
                                                                                                                                                        <br />
                                                                                                                                                        <strong>Our mailing address is:</strong>
                                                                                                                                                        <br />
                                                                                                                                                        *|HTML:LIST_ADDRESS_HTML|**|END:IF|* 
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td valign="middle" id="utility">
                                                                                    <div mc:edit="std_utility">
                                                                                        &nbsp;<a href="*|ARCHIVE|*" target="_blank">view this in your browser</a> | <a href="*|UNSUB|*">unsubscribe from this list</a> | <a href="*|UPDATE_PROFILE|*">update subscription preferences</a>&nbsp;
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                        </table>
                                                                        <!-- // End Module: Transactional Footer \\ -->
                                                                    
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <!-- // End Template Footer \\ -->
                                                        </td>
                                                    </tr>
                                                </table>
                                                <br />
                                            </td>
                                        </tr>
                                    </table>
                                </center>
                            </body>
                        </html>                        
                    """
            
        elif self._validFranchiseeCode['flag'] == False:
            body = "Hello, %s, and thanks for signing up for an \n elevatusventas.com account!\n\nTo activate your account, click this link within 48 \hours:\n\nhttp://example.com/accounts/confirm/%s" % (
                        self._identification,
                        self._activationKey)
         
        message =  EmailMessage(subject, body, mail, [self._email])
        message.content_subtype = "html"  # Main content is now text/html
        message.send()
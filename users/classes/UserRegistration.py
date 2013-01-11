# -*- coding: utf-8 -*-
from users.forms import RegistrationFormFranchisee
import datetime, random, sha
from users.models import UserProfile
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
        
        if self._validFranchiseeCode['flag'] == True:
            
            user = UserProfile.objects.get(identification=self._validFranchiseeCode['id'])
            print user
            
            newProfile = UserProfile(
                        identification=self._user, activationKey=self._activationKey,
                        keyExpires=self._keyExpires, refFranchiseeCode=self._franchiseeCode,
                        refFranchisee=user)
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
                                
                                                        /* /\/\/\/\/\/\/\/\/\/\ STANDARD STYLING: PREHEADER /\/\/\/\/\/\/\/\/\/\ */
                                
                                                        /**
                                                        * @tab Header
                                                        * @section preheader style
                                                        * @tip Set the background color for your email's preheader area.
                                                        * @theme page
                                                        */
                                                        #templatePreheader{
                                                                /*@editable*/ background-color:#FAFAFA;
                                                        }
                                
                                                        /**
                                                        * @tab Header
                                                        * @section preheader text
                                                        * @tip Set the styling for your email's preheader text. Choose a size and color that is easy to read.
                                                        */
                                                        .preheaderContent div{
                                                                /*@editable*/ color:#505050;
                                                                /*@editable*/ font-family:Arial;
                                                                /*@editable*/ font-size:10px;
                                                                /*@editable*/ line-height:100%;
                                                                /*@editable*/ text-align:left;
                                                        }
                                
                                                        /**
                                                        * @tab Header
                                                        * @section preheader link
                                                        * @tip Set the styling for your email's preheader links. Choose a color that helps them stand out from your text.
                                                        */
                                                        .preheaderContent div a:link, .preheaderContent div a:visited, /* Yahoo! Mail Override */ .preheaderContent div a .yshortcuts /* Yahoo! Mail Override */{
                                                                /*@editable*/ color:#336699;
                                                                /*@editable*/ font-weight:normal;
                                                                /*@editable*/ text-decoration:underline;
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
                                                                /*@editable*/ text-align:left;
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
                                                        * @section social bar style
                                                        * @tip Set the background color and border for your email's footer social bar.
                                                        * @theme footer
                                                        */
                                                        #social{
                                                                /*@editable*/ background-color:#FAFAFA;
                                                                /*@editable*/ border:0;
                                                        }
                                
                                                        /**
                                                        * @tab Footer
                                                        * @section social bar style
                                                        * @tip Set the background color and border for your email's footer social bar.
                                                        */
                                                        #social div{
                                                                /*@editable*/ text-align:center;
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
                                                        <td align="center" valign="top">
                                                        <!-- // Begin Template Preheader \\ -->
                                                        <table border="0" cellpadding="10" cellspacing="0" width="600" id="templatePreheader">
                                                            <tr>
                                                                <td valign="top" class="preheaderContent">
                                                                
                                                                        <!-- // Begin Module: Standard Preheader \ -->
                                                                    <table border="0" cellpadding="10" cellspacing="0" width="100%">
                                                                        <tr>
                                                                                <td valign="top">
                                                                                <div mc:edit="std_preheader_content">
                                                                                         Use this area to offer a short teaser of your email's content. Text here will show in the preview area of some email clients.
                                                                                </div>
                                                                            </td>
                                                                            <!-- *|IFNOT:ARCHIVE_PAGE|* -->
                                                                                                                        <td valign="top" width="190">
                                                                                <div mc:edit="std_preheader_links">
                                                                                        Is this email not displaying correctly?<br /><a href="*|ARCHIVE|*" target="_blank">View it in your browser</a>.
                                                                                </div>
                                                                            </td>
                                                                                                                        <!-- *|END:IF|* -->
                                                                        </tr>
                                                                    </table>
                                                                        <!-- // End Module: Standard Preheader \ -->
                                                                
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <!-- // End Template Preheader \\ -->
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
                                                                            <td valign="top" class="bodyContent">
                                                                
                                                                                <!-- // Begin Module: Standard Content \\ -->
                                                                                <table border="0" cellpadding="20" cellspacing="0" width="100%">
                                                                                    <tr>
                                                                                        <td valign="top">
                                                                                            <div mc:edit="std_content00">
                                                                                                <h1 class="h1">Heading 1</h1>
                                                                                                <h2 class="h2">Heading 2</h2>
                                                                                                <h3 class="h3">Heading 3</h3>
                                                                                                <h4 class="h4">Heading 4</h4>
                                                                                                <strong>Getting started:</strong> Customize your template by clicking on the style editor tabs up above. Set your fonts, colors, and styles. After setting your styling is all done you can click here in this area, delete the text, and start adding your own awesome content!
                                                                                                <br />
                                                                                                <br />
                                                                                                After you enter your content, highlight the text you want to style and select the options you set in the style editor in the "styles" drop down box. Want to <a href="http://www.mailchimp.com/kb/article/im-using-the-style-designer-and-i-cant-get-my-formatting-to-change" target="_blank">get rid of styling on a bit of text</a>, but having trouble doing it? Just use the "remove formatting" button to strip the text of any formatting and reset your style.
                                                                                            </div>
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
                                                                            
                                                                                <!-- // Begin Module: Standard Footer \\ -->
                                                                                <table border="0" cellpadding="10" cellspacing="0" width="100%">
                                                                                    <tr>
                                                                                        <td colspan="2" valign="middle" id="social">
                                                                                            <div mc:edit="std_social">
                                                                                                &nbsp;<a href="*|TWITTER:PROFILEURL|*">follow on Twitter</a> | <a href="*|FACEBOOK:PROFILEURL|*">friend on Facebook</a> | <a href="*|FORWARD|*">forward to a friend</a>&nbsp;
                                                                                            </div>
                                                                                        </td>
                                                                                    </tr>
                                                                                    <tr>
                                                                                        <td valign="top" width="350">
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
                                                                                        <td valign="top" width="190" id="monkeyRewards">
                                                                                            <div mc:edit="monkeyrewards">
                                                                                                *|IF:REWARDS|* *|HTML:REWARDS|* *|END:IF|*
                                                                                            </div>
                                                                                        </td>
                                                                                    </tr>
                                                                                    <tr>
                                                                                        <td colspan="2" valign="middle" id="utility">
                                                                                            <div mc:edit="std_utility">
                                                                                                &nbsp;<a href="*|UNSUB|*">unsubscribe from this list</a> | <a href="*|UPDATE_PROFILE|*">update subscription preferences</a>&nbsp;
                                                                                            </div>
                                                                                        </td>
                                                                                    </tr>
                                                                                </table>
                                                                                <!-- // End Module: Standard Footer \\ -->
                                                                            
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
             
             bodys = """
                    <html>
                    <p><head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                    <title>Nettuts Email Newsletter</title>
                    <p><link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/css/bootstrap-combined.min.css" rel="stylesheet"></p>
                    <p><script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/js/bootstrap.min.js"></script></p>
                    </head></p>
                    <p><body></p>
                    <p><table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4"><tr><td></p>
                    <p><table id="top-message" cellpadding="20" cellspacing="0" width="600" align="center">
                    </table><!-- top message -->
                    <table id="main" cellpadding="0" cellspacing="15" bgcolor="ffffff" width="600" align="center">
                    </table><!-- main -->
                    <table id="bottom-message" cellpadding="20" cellspacing="0" width="600" align="center">
                    <div class="hero-unit">
                            <h1>Saludos Cucho</h1>
                            <p>Tagline</p>
                            <p>
                              <a class="btn btn-primary btn-large">
                                Learn more
                              </a>
                            </p>
                          </div>
                        </table><!-- bottom message --></p>
                        <p></tr></td></table><!-- wrapper --></p>
                        <p></body></p>
                        <p></html>
                        </p>
                    """
            
        elif self._validFranchiseeCode['flag'] == False:
            body = "Hello, %s, and thanks for signing up for an \n elevatusventas.com account!\n\nTo activate your account, click this link within 48 \hours:\n\nhttp://example.com/accounts/confirm/%s" % (
                        self._identification,
                        self._activationKey)
         
        message =  EmailMessage(subject, body, mail, [self._email])
        message.content_subtype = "html"  # Main content is now text/html
        message.send()
        #send_mail(subject, body, mail, [self._email])
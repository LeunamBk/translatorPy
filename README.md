# translator-Py
If executes opens a little popup window in the bottom right corner of your display. This applications enables you to translate highlighed text with pressing crtl+y into selected target language via google trnslate. Earlier version has used geoslate which isnt working anymore, since google restricted theire public api. Now Selenium is used with PhantomJS webbrowser. 
 - TODO: Privious version (on windows) used win32clipboard which enables to fetch selected text directly without having the           user to copy text first to clipboard -> select text and crtl + y was sufficient to translate. Build crossplatform           by freezing or as distro with this functionality (win = win32clipboard, linux = ctypes ??) 

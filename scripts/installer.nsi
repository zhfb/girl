!define APPNAME "AI女友"
!define VERSION "1.0.0"
!define COMPANY "AIGirlfriend Team"
!define WEBSITE "https://github.com"

!define APPNAME_SHORT "AIGirlfriend"
!define INSTALL_DIR "$PROGRAMFILES\${APPNAME}"
!define DATA_DIR "$APPDATA\${APPNAME_SHORT}"

Name "${APPNAME}"
OutFile "..\release\${APPNAME}_v${VERSION}_安装程序.exe"
InstallDir "${INSTALL_DIR}"
InstallDirRegKey HKLM "Software\${APPNAME}" "InstallPath"
RequestExecutionLevel admin
VIProductVersion "${VERSION}.0"
VIAddVersionKey "ProductName" "${APPNAME}"
VIAddVersionKey "CompanyName" "${COMPANY}"
VIAddVersionKey "LegalCopyright" "${COMPANY}"
VIAddVersionKey "FileDescription" "${APPNAME} Installation"
VIAddVersionKey "FileVersion" "${VERSION}"

!include "MUI2.nsh"

!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
!define MUI_WELCOMEPAGE_TITLE "欢迎使用 ${APPNAME} 安装向导"
!define MUI_WELCOMEPAGE_TEXT "本向导将指引你完成 ${APPNAME} 的安装。$\r$\n$\r$\n点击下一步继续。"
!define MUI_FINISHPAGE_TITLE "完成 ${APPNAME} 安装"
!define MUI_FINISHPAGE_TEXT "${APPNAME} 已成功安装到你的计算机。$\r$\n$\r$\n点击完成退出安装向导。"
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APPNAME_SHORT}.exe"
!define MUI_FINISHPAGE_RUN_TEXT "运行 ${APPNAME}"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\docs\使用说明.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

LangString DESC_SecMain ${LANG_ENGLISH} "主程序文件"
LangString DESC_SecDesktop ${LANG_ENGLISH} "创建桌面快捷方式"
LangString DESC_SecStartMenu ${LANG_ENGLISH} "创建开始菜单项"

Section "${APPNAME} (必需)" SecMain
    SectionIn RO
    SetOutPath "$INSTDIR"

    File /r "..\dist\AIGirlfriend\*"

    WriteUninstaller "$INSTDIR\uninstall.exe"

    WriteRegStr HKLM "Software\${APPNAME}" "InstallPath" "$INSTDIR"
    WriteRegStr HKLM "Software\${APPNAME}" "Version" "${VERSION}"

    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANY}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
SectionEnd

Section "桌面快捷方式" SecDesktop
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${APPNAME_SHORT}.exe"
SectionEnd

Section "开始菜单" SecStartMenu
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\${APPNAME_SHORT}.exe"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\卸载.lnk" "$INSTDIR\uninstall.exe"
SectionEnd

Section "Post" SecPost
    SetShellVarContext all
    CreateDirectory "${DATA_DIR}"
SectionEnd

Section -AdditionalIcons
    WriteIniStr "$INSTDIR\${APPNAME}.url" "InternetShortcut" "URL" "${WEBSITE}"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\uninstall.exe"
    Delete "$INSTDIR\${APPNAME}.url"

    Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
    Delete "$SMPROGRAMS\${APPNAME}\卸载.lnk"
    RMDir "$SMPROGRAMS\${APPNAME}"

    Delete "$DESKTOP\${APPNAME}.lnk"

    RMDir /r "$INSTDIR"

    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
    DeleteRegKey HKLM "Software\${APPNAME}"

    MessageBox MB_OK|MB_ICONINFORMATION "${APPNAME} 已成功卸载。$\n$\n注意：用户数据保留在 ${DATA_DIR}"
SectionEnd

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} $(DESC_SecStartMenu)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

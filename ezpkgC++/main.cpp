#include <iostream>
#include <cstdlib>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <unistd.h>
#include <algorithm>
#include <vector>
#include <pwd.h>
#include <sstream>
using namespace std;
// Function to execute a shell command and return the output as a string
std::string getUsername() {
    // Get the username of the current user
    struct passwd* pw = getpwuid(geteuid());
    return (pw != nullptr) ? std::string(pw->pw_name) : "unknown";
}


void removeNewlines(std::string& str) {
    // Remove newline characters
    str.erase(std::remove_if(str.begin(), str.end(), [](char c) {
        return c == '\n' || c == '\r';  // Predicate to remove both '\n' and '\r'
    }), str.end());
}

int chkpath(const std::string& thepath) {
    // Check if the path exists using access instead of ls
    return access(thepath.c_str(), F_OK);  // F_OK checks for existence
}


std::vector<std::string> splitString(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    std::stringstream ss(str);
    std::string token;

    while (std::getline(ss, token, delimiter)) {
        tokens.push_back(token);
    }

    return tokens;
}
// helpers ^ //
// START OF COMMANDS //
void install(string dpkg ,string tempath , string pkgpath){
string url = "https://ayinalienbruvinnitwenomechainsamaswaghettiliciousawesomesauce.online/" + dpkg + ".zip";
// curl -L "https://example.com/file.zip" -o /path/to/save/file.zip && unzip /path/to/save/file.zip -d /path/to/extract/
    string install_cmd = "curl -L \"" + url + "\" -o " + tempath + dpkg +".zip && unzip " + tempath + dpkg + ".zip -d " + pkgpath;
    string rm_cmd_temp = "rm -f " + tempath + dpkg + ".zip";
    system(install_cmd.c_str());
    system(rm_cmd_temp.c_str());
}
void update() {
    cout << "update" << endl;
}

void listpkg(std::string lpath) {
    if (lpath.empty()) {
        std::cerr << "Error: Path is empty!" << std::endl;
        return;
    }

    string command = "ls " + lpath;
    int result = system(command.c_str());
    if (result == -1) {
        std::cerr << "Error: system() failed to execute command." << std::endl;
    }
}
void uninstall(string udpkg,string pkgrmpath) {
    string cmd = "rm -r " + pkgrmpath + udpkg;  // Add a space after "-f"
    system(cmd.c_str());
}

void upload() {
    string url = "https://fastink.alwaysdata.net/upload";
    string msg = R"(
1- If you want to upload a Python file, please put it inside a folder named after the package. The folder and zip file should both have the same name as the package for installation using install <pkg>
2 - Enter package path (make sure to compress folder before upload) (only zip file's are allowed):
                    )";
    string zippath;
    std::string upload = "\033[1;32m#upload \033[0m\033[1;33m<pkg>\033[0m ~>";
    cout << upload;
    getline(cin, zippath);
    removeNewlines(zippath);
    std::string command = "curl -F \"file=@" + zippath + "\" " + url;  // Add @ for curl file upload
    system(command.c_str());  // Execute the command
}

int main() {
    std::string usr = getUsername();
    stringstream thepath;
    thepath << "/home/" << usr << "/ezpkg";
    string temppath = thepath.str() + "/temp/";
    string pkgpath = thepath.str() + "/packages/";
    int chkint = chkpath(thepath.str());  // convert here
    if (chkint > 0) {
        std::system("clear");
        std::cout << "\033[31mhmm.. it seems like ezpkg path is not found, lemme create it for you....\033[33m" << std::endl;
        string mkdir_command = "mkdir -p " + thepath.str() + "temp/ && mkdir -p " + thepath.str() + "packages";  // and here
        std::system(mkdir_command.c_str());
    } else {
        std::system("clear");
    }

    int id = getuid();
    if (id == 0) {
        cout << "\033[31mWARN:\033[33m program is running as sudo, please run it without sudo! Because it will not work!\033[0m" << std::endl;
        return 1;
    } else {
        std::system("clear");
    }
    while(true){
        string ezcmd;
    string ezpkg = "\033[1;32m#ezpkg \033[0m\033[1;33m<" + usr + ">\033[0m ~>";
    cout << ezpkg;
    getline(cin, ezcmd);
    removeNewlines(ezcmd);

    // makes the string all lowercase
    std::transform(ezcmd.begin(), ezcmd.end(), ezcmd.begin(),
    [](unsigned char c) { return std::tolower(c); });

    // a vector that splits a string
    vector<string> cmd = splitString(ezcmd, ' ');


    // commands
    if (cmd.size() > 1 && cmd[0] == "install" || cmd.size() > 1 && cmd[0] == "download") {
        install(cmd[1], temppath, pkgpath);
    } else if (cmd.size() == 1 && cmd[0] == "upload") {
        upload();
    }   else if (cmd.size() == 1 && cmd[0] == "exit" || cmd.size() == 1 && cmd[0] == "break") {
    return 0;
}
    else if (cmd.size() == 1 && cmd[0] == "ls" || cmd.size() == 1 && cmd[0] == "list") {
        listpkg(pkgpath);
    } else if (cmd.size() == 1 && cmd[0] == "update" || cmd.size() == 1 && cmd[0] == "upgrade") {
        update();
    } else if (cmd.size() > 1 && cmd[0] == "rm" || cmd.size() > 1 && cmd[0] == "uninstall" || cmd.size() > 1 && cmd[0] == "delete") {
        uninstall(cmd[1],pkgpath);
    }
    }

}


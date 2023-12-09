#include <bits/stdc++.h>
#include <iostream>
#include <sstream>
#include <map>
#include <vector>
#include <algorithm>

using namespace std;

string rename(string name) {
    for (int i = 0; i < name.size(); i++) {
        name[i] = tolower(name[i]);
    }
    stringstream ss(name);
    string token;
    string res = "";

    
    while (ss >> token) {
        token[0] = toupper(token[0]);
        res += token;

        // Check if there are more words to append a space
        if (ss >> ws) {
            res += " ";
        }
    }

    return res;
}

int main() {
    cout << rename("pJi kOjf KhOng");

    return 0;
}

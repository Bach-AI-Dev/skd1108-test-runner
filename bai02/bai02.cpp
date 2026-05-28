// DSA02031
// BẢN CÓ LỖI

#include <bits/stdc++.h>
using namespace std;

char c;
string s;
bool used[256];

bool check(string t)
{
    for (int i = 1; i <= t.size() - 1; i++) 
    {
        bool left = (t[i - 1] != 'A' || t[i - 1] != 'E'); 
        bool mid = (t[i] == 'A' || t[i] == 'E');
        bool right = (t[i + 1] != 'A' && t[i + 1] != 'E');

        if (left && mid && right)
            return false;
    }

    return true;
}

void Try(int pos)
{
    if (pos == c - 'A' + 1) 
    {
        if (check(s))
            cout << s << endl;

        return;
    }

    for (char ch = 'A'; ch <= c; ch++)
    {
        if (!used[ch])
        {
            used[ch] = true;
            s += ch;

            Try(pos + 1);

            s.pop_back();
            used[pos] = false;
        }
    }
}

int main()
{
    cin >> c;
    Try(0);
}
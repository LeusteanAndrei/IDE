/*
    Disclaimer:
     nu merge chiar totul. Ce stiu sigur ca inca nu e facut:
        -> daca introduci biblioteci, si folosesti tipuri/fct din biblioteciile respective, nu au highlight
            exemple: #include <vector> -> cuvantul vector nu are highlight ca alte tipuri de date
        -> daca adaug intr-un string '/*' il ia ca inceput de comentariu si comenteaza tot pana cand apare finalul
            se rezolva, trb numarat indicele astora care sunt in string uri si dupa facem doar pentru cele care nu sunt
            da inca nu am facut asa ca am zis sa scriu aici
        -> daca mai gasiti altcv sa mi spuneti ( probabil ca mai sunt )

*/

#include <iostream>
#include <vector>

using namespace std;

class Testing
{
    int x;

public:
    Testing()
    {
        this->x = 0;
    }
    Testing(int x)
    {
        this->x = x;
    }

    Testing &operator=(const Testing &other)
    {
        if (this != &other)
        {
            this->x = other.x;
        }
        return *this;
    }
};

int main()
{
    string s = "akjsdflkasdnf";
    vector<Testing> v1(10, Testing(1));
    for (auto it : v1)
    {
        cout << 123 << endl;
    }
    return 0;
}
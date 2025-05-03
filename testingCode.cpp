
#include <iostream>
#include <string.h>

using namespace std;
class clasa
{
public:
	int y;

	clasa()
	{
		this->y = 0;
	}

	void	functie(int x, int m)
	{
		cout<<"heibei";
	}

};

int main()
{
	clasa c ;
           int x = 2;
	c.functie(2, 3);
}
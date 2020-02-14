#include "R_LogOut.hpp"
#include "ModuleTest.hpp"
#include "csv_reader.h"
#include <stdio>
//#include "Fake.hpp"


R_LogOut g_LogOut;

void ModuleTestClass::TestMethod()
{
    CSV_Reader("c:\\Temp\\Plik.csv");
    CSV_Reader.ReadLine();


}

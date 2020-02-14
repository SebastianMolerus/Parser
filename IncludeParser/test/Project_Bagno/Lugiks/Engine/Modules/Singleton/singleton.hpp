#ifndef SINGLETON_HPP
#define SINGLETON_HPP
#include "ICSVFileReader.h"
#include "csv_reader.h"


class Singleton
{
public:
    static &Singleton GetInstance()
	{
		static Singleton s;
		return s;
	}

private:
	Singleton();
};

#endif // SINGLETON_HPP
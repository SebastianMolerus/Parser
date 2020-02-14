#ifndef ICSVFILEREADER_H
#define ICSVFILEREADER_H
#include <string>

struct ICSVFileReader
{
    ~ICSVFileReader() {}
    virtual bool ReadLine(std::string &rLine) = 0;
};
#endif // ICSVFILEREADER_H

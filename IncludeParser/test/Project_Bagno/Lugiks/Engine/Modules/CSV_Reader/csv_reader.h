#ifndef CSV_READER_H
#define CSV_READER_H
#include <string>
#include <fstream>
#include <sstream>
#include "ICSVFileReader.h"


class CSV_Reader : public ICSVFileReader
{
public:
    CSV_Reader(const std::string &filePath);

    ~CSV_Reader();

    virtual bool ReadLine(std::string &rLine);

private:
    void OpenCSVFile(const std::string &filePath);

    std::fstream m_CsvFileInput;
    bool m_GoodData;
};

#endif // CSV_READER_H

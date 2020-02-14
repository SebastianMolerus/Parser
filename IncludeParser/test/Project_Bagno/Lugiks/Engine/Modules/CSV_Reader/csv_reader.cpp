#include "csv_reader.h"
#include <iostream>

CSV_Reader::CSV_Reader(const std::string &filePath) : m_GoodData(false)
{
    std::cout << " ..::CSV Reader::.." << std::endl;
    OpenCSVFile(filePath);
}

CSV_Reader::~CSV_Reader()
{
    m_CsvFileInput.close();
}

void CSV_Reader::OpenCSVFile(const std::string &filePath)
{
    m_CsvFileInput.open(filePath.c_str(), std::ios::in);
    if(!m_CsvFileInput.is_open())
    {
        m_GoodData = false;
    }

    //Empty file
    if(m_CsvFileInput.peek() == std::ifstream::traits_type::eof())
    {
        m_GoodData = false;
    }

    m_GoodData = true;
}

bool CSV_Reader::ReadLine(std::string &rLine)
{
    if(m_CsvFileInput.eof() || m_GoodData == false)
    {
        return false;
    }

    getline(m_CsvFileInput, rLine);

    if(rLine.empty())
    {
        return false;
    }
    return true;
}

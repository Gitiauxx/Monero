#include <iostream>


#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string> 
#include <unordered_map>


class CSVKey
{
public:
	std::string const& operator[](std::size_t index) const
	{
		return m_data[index];
	}
	std::size_t size() const
	{
		return m_data.size();
	}
	void readNextRow(std::istream& str)
	{
		std::string         line;
		std::getline(str, line);

		std::stringstream   lineStream(line);
		std::string         cell;

		m_data.clear();

		while (std::getline(lineStream, cell, ','))
		{
			m_data.push_back(cell);
		}
		// This checks for a trailing comma with no data after it.
		if (!lineStream && cell.empty())
		{
			// If there was a trailing comma then add an empty element.
			m_data.push_back("");
		}
	}
private:
	std::vector<std::string>    m_data;
};


std::istream& operator>>(std::istream& str, CSVKey& data)
{
	data.readNextRow(str);
	return str;
}

// hash table to register real-spent key
std::unordered_map<std::string, int> matched;

void number_transaction(std::istream& file, std::string filename) {
	// each row is a input represented by a key in position 2 
	CSVKey input;
	std::string tx = "0";
	int count = 0;

	// go down one row to remove header
	file >> input;

	// open file_out for export
	std::ofstream file_out;
	file_out.open(filename);

	while (file >> input)
	{
		if (count == 0)
		{
			tx = input[4];
		}
		if (input[4] == tx)
		{
			count += 1;
		}
		else
		{
			file_out << tx << ";" << count << std::endl;
			tx = input[4];
			count = 1;
		}
	}
	file_out.close();
}


void zero_mixin(std::istream& file, std::istream& transactions) {

	// each row is a input represented by a key in position 2 
	CSVKey input;
	CSVKey tran;
	std::string key;
	std::string key_identified;
	int count = 0;
	int number_tx = 0;
	int counter_tx = 1;
	
	// go down one row to remove header
	file >> input;

	while (transactions >> tran) {
		number_tx = std::stoi(tran[1]);
		while (file >> input)
		{
			while (counter_tx <= number_tx)
			{
				// temporarily save all keys in this transaction
				// and count the ones already matched
				key = input[2];
				while ((matched.find(key) == matched.end()) & (count < 1))
				{
					count += 1;
					key_identified = key;
				}
			}
			// within a transaction look for key already match
			counter_tx = 1;
			if (count == 1) {
					matched[key_identified] = 1;
				}
			count = 0;
		}
	}
}
int main()
{
	std::ifstream  file("C:\\Users\\MX\\Documents\\Xavier\\Monero\\data\\data_monero_1400K.csv");
	std::string filename = "C:\\Users\\MX\\Documents\\Xavier\\Monero\\data\\transactions.csv";
	int real_spent_count = 0;
	int total = 0;

	number_transaction(file, filename);
	std::cout << total << '\n';
	std::cout << matched.size() << '\n';

	return 0;
}
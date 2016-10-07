require 'rubygems'
require 'mechanize'
require 'csv'
require 'Indirizzo'


# Note: Disclaimer page is http://casesearch.courts.state.md.us/inquiry/inquiry-index.jsp

COUNTY_CODES = { 
  "District Court" => 'DC',
  "Allegany County Circuit Court" => '01',
  "Anne Arundel County Circuit Court" => '02',
  "Baltimore City Circuit Court" => '24',
  "Baltimore County Circuit Court" => '03',
  "Calvert County Circuit Court" => '04',
  "Caroline County Circuit Court" => '05',
  "Carroll County Circuit Court" => '06',
  "Cecil County Circuit Court" => '07',
  "Charles County Circuit Court" => '08',
  "Dorchester County Circuit Court" => '09',
  "Frederick County Circuit Court" => '10',
  "Garrett County Circuit Court" => '11',
  "Harford County Circuit Court" => '12',
  "Howard County Circuit Court" => '13',
  "Kent County Circuit Court" => '14',
  "Montgomery County Circuit Court" => '15',
  "Prince George's County Circuit Court" => '16',
  "Queen Anne's County Circuit Court" => '17',
  "Saint Mary's County Circuit Court" => '18',
  "Somerset County Circuit Court" => '19',
  "Talbot County Circuit Court" => '20',
  "Washington County Circuit Court" => '21',
  "Wicomico County Circuit Court" => '22',
  "Worcester County Circuit Court"  => '23'
}

CASE_CODES = {
  'Foreclosure' => 'O'
}

# These may not all be necessary anymore (such as the blank strings), but were used for initial brainstorming. 
county_code = '24'
case_code = 'O'
case_number = '000001'
case_code_length = 6
title = ''
filing_date =''
property_addresses = []
unit_number = ''
house_number = ''
year = ''

puts "-- Maryland Judiciary Case Search Web Scraper --"
puts "This web scraper currently only searches foreclosure cases."
puts "Please enter the last two digits of the year you wish to search."
puts "For example, for the year 2013 you would enter '13': "
year = gets.chomp

# Data will be saved to "name_of_county_foreclosure_data_year.csv"
filename = COUNTY_CODES.invert[county_code].split[0..1].join('_').downcase + '_' + CASE_CODES.invert[case_code].downcase + '_data_' + "20#{year}" + '.csv'
puts "Your data will be saved to #{filename}"
options = { write_headers: true, headers: ['case_number','title', 'filing_date', 'amount', 'raw_address', 'house_number','street_1', 'unit_number', 'street_2', 'street_3', 'street_4', 'city', 'state', 'postal_code', 'plus4'] }

# The line items in the case record you are looking for, and their respective spellings
requested_items = { title: 'Title:', filing_date: 'Filing Date:', party_type: 'Property Address', org_name: 'Business or Organization Name:'}

agent = Mechanize.new

CSV.open(filename, 'w', options) do |f|
  # Currently there's no implementation for checking when the end of a year's records occur. So the scraper will keep iterating case numbers up to 4000. The user must keep an eye on the command line window. When a case starts repeating itself, it's time to CTRL+C end the script.
  while case_number.to_i < 4000
    # Let's visit the case search page with a normal HTTP GET request.
    agent.get 'http://casesearch.courts.state.md.us/inquiry/processDisclaimer.jis'
    
    # If visiting the main page takes us to the disclaimer page, we check the box and continue.
    if agent.page.form('main')
      disclaimer = agent.page.form 'main'
      disclaimer.checkbox_with(name: "disclaimer").check
      disclaimer.submit
      sleep 0.5
    end

    # Now that we're at the case search page...
    case_search = county_code + case_code + year + case_number
    # There a multiple forms on the page, find the form the makes inquiries by case number
    case_search_form = agent.page.form(name: 'inquiryFormByCaseNum')
    # Select the county (Baltimore City)
    case_search_form.locationCode = '24'
    # Enter the case_search number we generated on line 75
    case_search_form.caseId = case_search
    # Submit the form
    case_search_form.submit
    
    # Now that we've submitted the form, we should be at the appropriate case record. Every field (both the titles and actual values) is wrapped in a <td> so let's pull them all from the page and throw them in an array.
    td = agent.page.parser.css 'td'

    # Now we iterate through each <td>
    td.each_with_index do |item, index| 

      # Inside each <td> is a <span> we need to look through to match our requested_items.
      if item.css('span').text == requested_items[:title]
        title = td[index+1].css('span').text
      end

      if item.css('span.Prompt').text == requested_items[:filing_date]
        filing_date = item.css('span')[2].text
      end
      
      # <td><span class="Value">Property Address</span><span class="Prompt">Party No.:</span><span class="Value">1</span></td>
      # becomes something like "Property Address1" for some reason...
      # Truncating the last two characters seems to fix this.
      if item.css('span.Value').text[0..-2] == requested_items[:party_type]
        # A case record might have multiple property addresses, so we put them all into an array.
        property_addresses << td[index+2].css('span').text
      end
    end

    # Once we've put all the property addresses into the array, we iterate through that array.
    property_addresses.each do |a|

      # The next set of lines parses out each individual address into appropriate fields.
      find_the_money = a.gsub(/\(/, '').gsub(/\)/, '').split('$')
      address = find_the_money[0]
      address = address.gsub('balto', ",baltimore").gsub('Balto', ",baltimore")
      address.empty? ? parsed_address = Indirizzo::Address.new(' ') : parsed_address = Indirizzo::Address.new(address)

      find_the_money.length > 1 ? money = find_the_money[1][0..-2] : money = ''

      if !parsed_address.street[0].nil? && parsed_address.street[0].include?(" unit ")
        unit_number = "unit " + parsed_address.street[0].split(" unit ")[0]
      end
      if !parsed_address.street[1].nil? && parsed_address.street[1].include?(" unit ")
        parsed_address.street[1] = parsed_address.street[1].split(' unit ')[0]
      end
      if !parsed_address.street[2].nil? && parsed_address.street[2].include?(" unit ")
        parsed_address.street[2] = parsed_address.street[2].split(' unit ')[0]
      end
      if !parsed_address.street[3].nil? && parsed_address.street[3].include?(" unit ")
        parsed_address.street[3] = parsed_address.street[3].split(' unit ')[0]
      end

      # Once a property address is all parsed out, we add a new line to the csv file.
      f << [case_search, 
          title, 
          filing_date,
          money,
          address,
          parsed_address.nil? ? '' : parsed_address.number,
          parsed_address.nil? || parsed_address.street[0].nil? ? '': parsed_address.street[0],
          unit_number,
          parsed_address.nil? || parsed_address.street[1].nil? ? '': parsed_address.street[1],
          parsed_address.nil? || parsed_address.street[2].nil? ? '': parsed_address.street[2],
          parsed_address.nil? || parsed_address.street[3].nil? ? '': parsed_address.street[3],
          parsed_address.nil? || parsed_address.city[0] == parsed_address.street[0] ? "Baltimore" : parsed_address.city[0],
          "MD",
          parsed_address.nil? ? '' : parsed_address.zip,
          parsed_address.nil? ? '' : parsed_address.plus4,
        ]
    end

    ## This is to display some information for each record to the screen while we iterate.

    #puts "-------------------------- Case Information ---------------------------"
    puts "Case number: #{case_number}\t\tTitle: #{title}"
    #puts "Filing Date: #{filing_date}\t\tMoney: #{money.nil? ? "Not Found" : money}"
    #puts "Raw Address: #{address}"
    #puts "House Number: #{parsed_address.number}\t\tStreet: #{parsed_address.street[0]}"
    #puts "City: #{parsed_address.city[0] == parsed_address.street[0] ? 'Baltimore' : parsed_address.city[0]}\t\tState: #{parsed_address.state}"
    #puts "Postal Code: #{parsed_address.zip}"
    #puts "------------------------------------------------------------------------"

    # Make the array of property addresses empty for the next case record search.
    property_addresses = []

    # So we don't overwhelm the Maryland case search system, or potentially get flagged for abuse, sleep for 300 milliseconds between each search to look more like a human user.
    sleep 0.3

    case_number.succ!
  end
end


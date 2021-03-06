from lib.google_search_results import GoogleSearchResults

# Documentation ~ https://serpapi.com/demo

"""
*NOTE* ~ Make sure every entry in 'serp_urls.txt' has this structure: [business name],[city],[state].

This is important because each entry is then saved to a list, delimiter split via comma, and each piece
added where needed in request.

"""

api_key = open('serp-api-key.txt').read()

downloadFile = 'gmb-status-crawl.csv'
file = open(downloadFile, 'w')

columnHeader = 'Query,Name,Address,Website,GMB Unclaimed?\n'
file.write(columnHeader)

with open('serp_urls.txt') as content:
    content = [line.rstrip('\n') for line in content]
    content = [line.split(",") for line in content]

    for line in content:
        errorType = ''
        params = {
            "q" : str(line[0]),
            "location" : f"{line[1]},{line[2]},United States",
            "hl" : "en",
            "gl" : "us",
            "google_domain" : "google.com",
            "api_key" : api_key,
        }

        query = GoogleSearchResults(params)
        dictionary_results = query.get_dictionary()
        # print(dictionary_results['knowledge_graph'])
        query = "{} {} {}".format(line[0], line[1], line[2])

        try:
            name = dictionary_results['knowledge_graph']['title']
            address = dictionary_results['knowledge_graph']['address']
            website = dictionary_results['knowledge_graph']['website']
        except KeyError:
            errorType = 'Error'
            row = f'"{query}" ~ No Listing Exists\n'
            print(f'{query} ~ No Listing Exists')
            file.write(row)

        if errorType != 'Error':
            name = dictionary_results['knowledge_graph']['title']
            address = dictionary_results['knowledge_graph']['address']
            website = dictionary_results['knowledge_graph']['website']

            try:
                listingStatus = dictionary_results['knowledge_graph']['unclaimed_listing']
            except KeyError as e:
                listingStatus = 'FALSE'
                row1 = f'"{query}","{name}","{address}",{website},{listingStatus}\n'
                file.write(row1)
                print(row1)
            else:
                name = dictionary_results['knowledge_graph']['title']
                address = dictionary_results['knowledge_graph']['address']
                website = dictionary_results['knowledge_graph']['website']
                listingStatus = dictionary_results['knowledge_graph']['unclaimed_listing']

                row = f'{query},"{name}","{address}",{website},{listingStatus}\n'
                file.write(row)
                print(row)

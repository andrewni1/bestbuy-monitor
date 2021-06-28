with open('productList.txt') as f:
        for line in f:
            line = line.strip()
            productURL = line

            print(productURL)
            
            
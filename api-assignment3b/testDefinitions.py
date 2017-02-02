from base_page import BaseHandler

class TestDefinitions(BaseHandler):

	base_url = "https://api-assignment3b.appspot.com"
	#base_url = "http://localhost:8080"
	customers_url = "/customers"
	orders_url = "/orders"
	products_url = "/products"

	bad_key = '999999999999360'

	load_customer_list = [
		{
			"firstname": "April",
			"lastname": "May",
			"email": "juneJuly@gmail.com"
		},
		{
			"firstname": "Carmen",
			"lastname": "Green",
			"email": "carmengreen@gmail.com"
		},
		{
			"firstname": "May",
			"lastname": "Balleen",
			"email": "beauty1@face.com"
		},
		{
			"firstname": "Carrie",
			"lastname": "UnderGreen",
			"email": "carry_undergreen@apple.com"
		},
		{
			"firstname": "Ima",
			"lastname": "Person",
			"email": "ima.person.@gmail.com"
		},
				{
			"firstname": "April",
			"lastname": "May2",
			"email": "juneJuly2@gmail.com"
		},
		{
			"firstname": "Carmen",
			"lastname": "Green2",
			"email": "carmengreen2@gmail.com"
		},
		{
			"firstname": "May",
			"lastname": "Balleen2",
			"email": "beauty12@face.com"
		},
		{
			"firstname": "Carrie",
			"lastname": "UnderGreen2",
			"email": "carry_undergreen2@apple.com"
		},
		{
			"firstname": "Ima",
			"lastname": "Person2",
			"email": "ima.person.2@gmail.com"
		}
	]

	good_update_list = {
		"firstname": {'firstname':"Wally"},
		"lastname": {'lastname':"Wassermann"},
		"email": {'email':"wallywassermann@gmail.com"}
	}

	good_update_product_list = {
		"sku": {'sku':"SKU0001"},
		"name": {'name':"My Updated Product"},
		"description":{"description":"My Updated Description"},
		"cost":{"cost":"399"},
		"quantity":{"quantity":"450"}
	}

	bad_update_list = {
		"firstname": {"firstname": "Ja*ne"},
		"lastname": {"lastname": "D*oe"},
		"email": {"email": "janedoegmail.com"},
		"duplicateemail": {"email":"mary.Kay@mary.kay.com"}
	}

	bad_update_product_list = {
		"sku": {'sku':"SK*U0001"},
		"duplicatesku":{'sku':"Prod0002"},
		"name": {'name':"My Updated* Product"},
		"description":{"description":"My Updated Description*"},
		"cost":{"cost":"39a"},
		"quantity":{"quantity":"45b"}
	}

	good_customer_list = [
		{
			"firstname": "Jane",
			"lastname": "Doe",
			"email": "janedoe@gmail.com"
		},
		{
			"firstname": "John",
			"lastname": "Doe",
			"email": "johndoe1@gmail.com"
		},
		{
			"firstname": "Mary",
			"lastname": "Kay",
			"email": "mary.Kay@mary.kay.com"
		},
		{
			"firstname": "Jennifer",
			"lastname": "apiGuru",
			"email": "jennifer_Guru@guru.com"
		},
		{
			"firstname": "Jumble",
			"lastname": "Person",
			"email": "jumble.person.1@gmail.com"
		}
	]

	good_product_list = [
		{
			'sku':"Prod0001",
			'name':"My Prod0001",
			"description":"My Prod0001 Description",
			"cost":"365",
			"quantity":"10"
		},
		{
			'sku':"Prod0002",
			'name':"My Prod0002",
			"description":"My Prod0002 Description",
			"cost":"35",
		},
		{
			'sku':"Prod0003",
			'name':"My Prod0003",
			"description":"My Prod0003 Description",
			"cost":"35",
			"quantity":"99"
		},
		{
			'sku':"Prod0004",
			'name':"My Prod0004",
			"description":"My Prod0004 Description",
			"cost":"35",
			"quantity":"99"
		},
		{
			'sku':"Prod0005",
			'name':"My Prod0005",
			"description":"My Prod0005 Description",
			"cost":"3",
			"quantity":"99"
		},
		{
			'sku':"Prod0006",
			'name':"My Prod0006",
			"description":"My Prod0006 Description",
			"cost":"3",
			"quantity":"99"
		},
		{
			'sku':"Prod0007",
			'name':"My Prod0007",
			"description":"My Prod0007 Description",
			"cost":"3",
			"quantity":"99"
		},
		{
			'sku':"Prod0008",
			'name':"My Prod0008",
			"description":"My Prod0008 Description",
			"cost":"3",
			"quantity":"99"
		},
		{
			'sku':"Prod0009",
			'name':"My Prod0009",
			"description":"My Prod0009 Description",
			"cost":"3",
			"quantity":"99"
		},
		{
			'sku':"Prod0010",
			'name':"My Prod0010",
			"description":"My Prod0010 Description",
			"cost":"3",
			"quantity":"99"
		},
		{
			'sku':"Prod0011",
			'name':"My Prod0011",
			"description":"My Prod0011 Description",
			"cost":"3",
			"quantity":"99"
		}
	]

	load_product_list = [
		{
			'sku':"0001",
			'name':"My Prod0001",
			"description":"My Prod0001 Description",
			"cost":"365",
			"quantity":"10"
		},
		{
			'sku':"0002",
			'name':"My Prod0002",
			"description":"My Prod0002 Description",
			"cost":"35",
		},
		{
			'sku':"0003",
			'name':"My Prod0003",
			"description":"My Prod0003 Description",
			"cost":"35",
			"quantity":"99"
		},
		{
			'sku':"0004",
			'name':"My Prod0004",
			"description":"My Prod0004 Description",
			"cost":"35",
			"quantity":"99"
		},
		{
			'sku':"0005",
			'name':"My Prod0005",
			"description":"My Prod0005 Description",
			"cost":"3",
			"quantity":"99"
		},
		{
			'sku':"0006",
			'name':"My Prod0006",
			"description":"My Prod0006 Description",
			"cost":"3",
			"quantity":"99"
		},
		{
			'sku':"0007",
			'name':"My Prod0007",
			"description":"My Prod0007 Description",
			"cost":"3",
			"quantity":"99"
		},
		{
			'sku':"0008",
			'name':"My Prod0008",
			"description":"My Prod0008 Description",
			"cost":"3",
			"quantity":"99"
		},
		{
			'sku':"0009",
			'name':"My Prod0009",
			"description":"My Prod0009 Description",
			"cost":"3",
			"quantity":"99"
		},
		{
			'sku':"0010",
			'name':"My Prod0010",
			"description":"My Prod0010 Description",
			"cost":"3",
			"quantity":"99"
		},
		{
			'sku':"0011",
			'name':"My Prod0011",
			"description":"My Prod0011 Description",
			"cost":"3",
			"quantity":"99"
		}
	]

	erronous_customer_dict = {
		'bad_fname':
		{
			"firstname": "Jane*s",
			"lastname": "Doe",
			"email": "erronousjanedoe@gmail.com"
		},
		'bad_lname':
		{
			"firstname": "Janes",
			"lastname": "Doe*",
			"email": "erronousjanedoe@gmail.com"
		},
		'bad_email':
		{
			"firstname": "Janes",
			"lastname": "Doe",
			"email": "janedoe"
		}
	}

	missing_customer_dict = {
		'missing_fname':
		{
			"lastname": "Doe",
			"email": "janedoemissing@gmail.com"
		},
		'missing_lname':
		{
			"firstname": "John",
			"email": "johndoemissing@gmail.com"
		},
		'missing_email':
		{
			"firstname": "Mary",
			"lastname": "Kay"
		}
	}

	missing_product_dict = {
		'missing_sku':
		{
			'name':"My Prod0001",
			"description":"My Prod0001 Description",
			"cost":"365",
			"quantity":"10"
		},
		'missing_name':
		{
			'sku':"Prod0002",
			"description":"My Prod0002 Description",
			"cost":"35",
			"quantity":"1"
		},
		'missing_description':
		{
			'sku':"Prod0003",
			'name':"My Prod0003",
			"cost":"35",
			"quantity":"99"
		},
		'missing_cost':
		{
			'sku':"Prod0004",
			'name':"My Prod0004",
			"description":"My Prod0004 Description",
			"quantity":"99"
		}
	}

	erronous_product_dict = {
		'bad_sku':
		{
			'sku':"Prodx00*01",
			'name':"My Prod0001",
			"description":"My Prod0001 Description",
			"cost":"365",
			"quantity":"10"
		},
		'bad_name':
		{
			'sku':"Prodx0002",
			'name':"My Prod*0002",
			"description":"My Prod0002 Description",
			"cost":"35",
			"quantity":"1"
		},
		'bad_description':
		{
			'sku':"Prodx0003",
			'name':"My Prod0003",
			"description":"My Prod0003* Description",
			"cost":"35",
			"quantity":"99"
		},
		'bad_cost':
		{
			'sku':"Prodx0004",
			'name':"My Prod0004",
			"description":"My Prod0004 Description",
			"cost":"35a",
			"quantity":"99"
		},
		'bad_quantity':
		{
			'sku':"Prodx0005",
			'name':"My Prod0005",
			"description":"My Prod0005 Description",
			"cost":"3",
			"quantity":"aa"
		},
		'duplicate_sku':
		{
			'sku':"Prod0001",
			'name':"My Prod0005",
			"description":"My Prod0005 Description",
			"cost":"3",
			"quantity":"1"
		}
	}

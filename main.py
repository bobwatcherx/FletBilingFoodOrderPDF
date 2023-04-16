from flet import *
import random
import datetime
import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle



# NOW GET DATE NOW
now = datetime.datetime.now()
formated_date = now.strftime("%d-%m-%Y")



def main(page:Page):
	page.scroll = "auto"
	# CHANGE THEME
	page.theme_mode = "light"
	# YOU LIST ORDER FOOD 
	all_food =  Column()


	# ADD TO all_food
	def addtofood(e):
		# FOR PRICE I RANDOM PRICE 
		# from price 500 - 50000
		random_price = random.randint(500,10000)
		total_price = random_price * int(con_input.content.controls[4].value)


		all_food.controls.append(
			Container(
			padding=10,
			bgcolor="yellow200",
			content=Column([
			# NOW GET YOU INPUT FOOD NAME AND FOOD PCS ORDER
		Text(con_input.content.controls[3].value,
			weight="bold",size=20
			),
		# ADD PCS OF you FOOD ORDER
		Text(f"total buy{con_input.content.controls[4].value}",
			weight="bold",size=20
			),
		# NOW FOR TOTAL PRICE is you buy * random price
		Row([
		Text("total price",weight="bold"),
		Text(f"${'{:,.2f}'.format(total_price)}")

			],alignment="spaceBetween")
				])
			)
			)
		page.update()




	# CREATE CONTAINER FOR INPUT CUSTOMER ADDRESS

	con_input = Container(
	content=Column([
		TextField(label="username"),
		TextField(label="addres"),
		Text("input Order Food",size=25,weight="bold"),
		TextField(label="Food name"),
		TextField(label="You buy pcs"),
		ElevatedButton("add to food",
			on_click=addtofood
			)
		])
		)


	def savetomybiling(e:FilePickerResultEvent):
		you_file_save_location = e.path
		print(you_file_save_location)

		file_path = f"{you_file_save_location}.pdf"
		doc = SimpleDocTemplate(file_path,pagesizes=letter)

		elements = []


		styles =  getSampleStyleSheet()

		# AND NOW CREATE TITLE IN YoU PDF BILING FILE
		# elements.append(Paragraph("Biling order",styles['Title']))
		elements.append(Paragraph("Billing Order", styles["Title"]))
		
		customer_name = con_input.content.controls[0].value


		# NOW ADD NAME AND DATE ORDER TO PDF BILING
		elements.append(Paragraph(f"Name {customer_name}",styles['Normal']))
		# NOW FOR DATE ORDER CUSTOMER
		elements.append(Paragraph(f"Date order {formated_date}",styles['Normal']))
		

		# NOW FOR ADDRESS
		addresss = con_input.content.controls[1].value
		elements.append(Paragraph(f"address : {addresss}",styles['Normal']))
		
		elements.append(Paragraph("You Order Food",styles['Heading1']))


		list_order = []
		list_order.append(["Food name","pcs","price"])


		# NOW LOOP FOOD ORDER AND APPEND TO list_order
		for b in all_food.controls:
			list_order.append([
			b.content.controls[0].value,
			# FOR PRICE REPLACE AND HIDE $

			b.content.controls[1].value.replace('$', '').replace(',', ''),
			# THIS FOR TOTAL ALL YOU PRICE ORDER OR GRAND TOTAL
			# YOU ORDER FOOD

			b.content.controls[2].controls[1].value.replace('$', '').replace(',', ''),
				])

		table = Table(list_order)

		# NOW THIS OPTIONAL IF YOU STYLE THE TABLE ORDER IN PDF FILE

		table.setStyle(TableStyle([
			("BACKGROUND",(0,0),(-1,0),colors.grey),
			("TEXTCOLOR",(0,0),(-1,0),colors.whitesmoke),
			("ALIGN",(0,0),(-1,0),"CENTER"),
			("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
			("FONTSIZE",(0,0),(-1,0),14),
			("BOTTOMPADDING",(0,0),(-1,0),12),
			("BACKGROUND",(0,0),(-1,-1),colors.beige),
			("TEXTCOLOR",(0,0),(-1,-1),colors.black),
			("ALIGN",(0,0),(-1,-1),"RIGHT"),
			("FONTNAME",(0,0),(-1,-1),"Helvetica"),
			("FONTSIZE",(0,0),(-1,-1),12),
			("BOTTOMPADDING",(0,0),(-1,-1),8),

			]))

		elements.append(table)
		grand_total = sum([float(row[2]) for row in list_order[1:]])
		
		# NOW ADD grand_total TO PDF FILE

		elements.append(Paragraph(f'grand total : ${grand_total:.2f}',styles['Heading1']))

		# NOW BUILD PDF 
		doc.build(elements)



















	# NOW FOR SAVE ADD FILE PICKER FOR SAVE YoU BILING
	file_saver = FilePicker(
		on_result=savetomybiling
		)
	page.overlay.append(file_saver)

	def buildmyorder(e):
		# NOW FOR SEE YOU ORDER 
		# OPEN DIALOG 
		mydialog = AlertDialog(
		title=Text("Biling order",size=30,weight="bold"),
		content=Column([
			# NOW GET NAME ADDRESS AND DATE NOW YOU ORDER NOW
			Row([
			# GET NAME
			Text(con_input.content.controls[0].value,
				weight="bold",size=20
				),

			# FOR DATE NOW yoU ORDER
			Text(f"Order date : {formated_date}",
				weight="bold"
				),
				]),

			# NOW GET ADDRESS yoU INPUT
			Row([
				Text("address",weight="bold"),
				Text(con_input.content.controls[1].value,
					weight="bold"
					),
			],alignment="end"),
			Text("You Order Burger",weight="bold",size=25),
			# YoU LIST FOOD HERE
			all_food

			],scroll="auto"),

		# AND NOW ADD PRINT MY BILING BUTTON
		actions=[
		ElevatedButton("print my biling",
			bgcolor="yellow",
			on_click=lambda e:file_saver.save_file()
			)

		]
			)
		page.dialog = mydialog
		mydialog.open = True
		page.update()






	# NOW CREATE FLOATING ACTION BUTTON FOR SEE RESULT ORDER
	page.floating_action_button = FloatingActionButton(
		icon="add",bgcolor="yellow",
		on_click=buildmyorder
		)


	page.add(
		Column([
			con_input,
			Text("You Burger Oder",weight="bold",size=20),
			all_food

			])
		)

flet.app(target=main)

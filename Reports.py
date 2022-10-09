from PIL import Image
from fpdf import FPDF

File_Name = ['Protocol', 'Data', 'PIE_CAll', 'Map', 'TECH', 'BAR_CALL', 'RSRP', 'SINR', ]
logo = Image.open(r"LOGO.png").convert("RGBA")
logo_M = Image.open(r"LOGO_MAIN.png").convert("RGBA")



def Generate_Report(fig_array):
    # Images File Names
    pdf = FPDF()
    for plot in fig_array:
        plot.write_image("assets/images/" + File_Name[fig_array.index(plot)] + ".jpeg", width=1122.5, height=794)
        cover = Image.open('assets/images/' + File_Name[fig_array.index(plot)] + ".jpeg")
        cover.paste(logo, (1080, 760,), logo)
        cover.paste(logo_M, (455, 15,), logo_M)
        cover.save("assets/images/" + File_Name[fig_array.index(plot)] + ".jpeg", format='jpeg')
        width, height = cover.size

        # convert pixel in mm with 1px=0.264583 mm
        width, height = float(width * 0.264583), float(height * 0.264583)

        # given we are working with A4 format size
        pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

        # get page orientation from image size
        orientation = 'P' if width < height else 'L'

        #  make sure image size is not greater than the pdf format size
        width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
        height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']

        pdf.add_page(orientation=orientation)

        pdf.image('assets/images/' + File_Name[fig_array.index(plot)] + ".jpeg", 0, 0, width, height)
    print("Report Created")
    return pdf



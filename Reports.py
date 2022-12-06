from PIL import Image
from fpdf import FPDF

NEW_FIG_ARRAY = []
File_Name = ['Protocol', 'Data', 'PIE_CAll', 'Map', 'TECH', 'BAR_CALL', 'RSRP', 'SINR', ]
logo = Image.open(r"IMAGES/LOGO.png").convert("RGBA")
logo_M = Image.open(r"IMAGES/LOGO_MAIN.png").convert("RGBA")


def Generate_Report(fig_array):
    NEW_FIG_ARRAY = fig_array
    # Images File Names
    pdf = FPDF()
    for plot in NEW_FIG_ARRAY:
        plot.write_image("IMAGES/" + File_Name[NEW_FIG_ARRAY.index(plot)] + ".png", width=1122.5, height=794)
        cover = Image.open('IMAGES/' + File_Name[NEW_FIG_ARRAY.index(plot)] + ".png")
        cover.paste(logo, (1080, 760,), logo)
        cover.paste(logo_M, (455, 15,), logo_M)
        cover.save("IMAGES/" + File_Name[NEW_FIG_ARRAY.index(plot)] + ".png", format='png')
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

        pdf.image('IMAGES/' + File_Name[NEW_FIG_ARRAY.index(plot)] + ".png", 0, 0, width, height)
    return pdf

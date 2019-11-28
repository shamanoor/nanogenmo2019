import reportlab.rl_config
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.flowables import DocAssign, Image, PageBreak

reportlab.rl_config.warnOnMissingFontGlyphs = 0
import PIL

pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

registerFontFamily('Vera', normal='Vera', bold='VeraBd', italic='VeraIt', boldItalic='VeraBI')

font_file = 'Symbola.ttf'
symbola_font = TTFont('Symbola', font_file)
pdfmetrics.registerFont(symbola_font)

normal = ParagraphStyle(name="Normal", fontName="Symbola", fontSize=12, leading=11)
title = ParagraphStyle(name="Title", fontName="Helvetica", fontSize=42, leftIndent=50)
header = ParagraphStyle(name='Header', fontName="Symbola", fontSize=18, leading=11)


def prepare_images():
    imgs = ['img/angry_romeo.jpg', 'img/happy_romeo.jpg', 'img/neutral_romeo.jpg', 'img/angry_juliet.jpg',
            'img/happy_juliet.jpg', 'img/neutral_juliet.jpg']

    for i in range(len(imgs)):
        img = PIL.Image.open(imgs[i])
        new_img = img.resize((120, 120))
        new_img.save('img_resized/' + imgs[i][4:], "jpeg", optimize=True)


def generate_pdf(file):
    with open(file, 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', '<br/>') \
            .replace('Juliet: <Media weggelaten> Neutral', 'Juliet: ' + 1 * "<br/>" + 11 * '<br/>' +
                     '<img src= "img_resized/neutral_juliet.jpg"/>' + 1 * '<br/>') \
            .replace('Juliet: <Media weggelaten> Positive', 'Juliet: ' + 1 * "<br/>" + 11 * '<br/>' +
                     '<img src= "img_resized/happy_juliet.jpg"/>' + 1 * '<br/>') \
            .replace('Juliet: <Media weggelaten> Negative', 'Juliet: ' + 1 * "<br/>" + 11 * '<br/>' +
                     '<img src= "img_resized/angry_juliet.jpg"/>' + 1 * '<br/>') \
            .replace('Romeo: <Media weggelaten> Neutral', 'Romeo: ' + 1 * "<br/>" + 11 * '<br/>' +
                     '<img src= "img_resized/neutral_romeo.jpg"/>' + 1 * '<br/>') \
            .replace('Romeo: <Media weggelaten> Positive', 'Romeo: ' + 1 * "<br/>" + 11 * '<br/>' +
                     '<img src= "img_resized/happy_romeo.jpg"/>' + 1 * '<br/>') \
            .replace('Romeo: <Media weggelaten> Negative', 'Romeo: ' + 1 * "<br/>" + 11 * '<br/>' +
                     '<img src= "img_resized/angry_romeo.jpg"/>' + 1 * '<br/>')

    story = [
        DocAssign("currentFrame", "doc.frame.id"),
        DocAssign("currentPageTemplate", "doc.pageTemplate.id"),
        DocAssign("aW", "availableWidth"),
        DocAssign("aH", "availableHeight"),
        DocAssign("aWH", "availableWidth,availableHeight"),
        Paragraph("<b>Romeo and Juliet</b>" + 15 * '<br/>', title),
        Image('img/romeo_juliet.jpg', width=4 * inch, height=5 * inch),
        PageBreak(),
        Paragraph("<b>Introduction</b>", header),
        Paragraph(
            2 * '<br/>' + "<i>A 2019 interpretation of the famous love story in the form of a WhatsApp dialogue. Made for NaNoGenMo.</i>",
            normal),
        PageBreak(),
        Paragraph(data, normal)
    ]

    doc = SimpleDocTemplate("romeo_and_juliet.pdf")
    doc.build(story)

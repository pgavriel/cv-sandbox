from layer import Layer
from path import Path
from clockanimator import ClockAnimator
import cv2 as cv

# Layer Image Setup
l_imgs = []
im_file = "img/tail5.png"
spinner = cv.imread(im_file,cv.IMREAD_UNCHANGED)
# spinner = ut.scale_image(spinner,25)

l_imgs.append([spinner, im_file])
i_select = 0

# SET A =======================================================
# Clock 1
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [244, 413]
layer.scale = 0.25
p1 = Path([[237, 522], [236, 577], [269, 600], [240, 611], [254, 622]],180)
p2 = Path([[281, 517], [287, 534], [287, 560], [298, 569], [284, 575], [298, 587]],157.5)
p3 = Path([[317, 493], [333, 510], [333, 544], [367, 569]],135)
c1 = ClockAnimator(layer,[p1,p2,p3])

# Clock 2
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [174, 538]
layer.scale = 0.0764555010917055
p1 = Path([[202, 559], [214, 566], [214, 584], [238, 602], [208, 614]],130)
p2 = Path([[180, 571], [181, 579], [182, 596], [188, 601], [183, 604], [198, 615]],175)
p3 = Path([[157, 564], [148, 574], [148, 608], [179, 631], [157, 639], [200, 669]],217)
c2 = ClockAnimator(layer,[p1,p2,p3])

# Clock 3
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [117, 554]
layer.scale = 0.050919251511894394
p1 = Path([[125, 575], [131, 587], [131, 614], [149, 627], [134, 632], [193, 674]],158)
p2 = Path([[96, 562], [70, 573], [71, 635], [77, 648], [61, 654], [57, 674]],252)
c3 = ClockAnimator(layer,[p1,p2])

# Clock 4
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [102, 512]
layer.scale = 0.04595462448948469
p1 = Path([[83, 516], [50, 522], [50, 642], [55, 649], [52, 673]],257)
c4 = ClockAnimator(layer,[p1])

# Clock 5
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [370, 476]
layer.scale = 0.050919251511894394
p1 = Path([[389, 488], [396, 493], [396, 520], [402, 525], [359, 540], [381, 556], [380, 572]],122)
c5 = ClockAnimator(layer,[p1])

# Clock 6
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [374, 418]
layer.scale = 0.03369641961943989
p1 = Path([[388, 418], [401, 418], [401, 517], [414, 527], [382, 540], [398, 552], [393, 572]],92)
c6 = ClockAnimator(layer,[p1])

clocks_a = [c1,c2,c3,c4,c5,c6]

# SET B =======================================================
# Clock 7
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [94, 333]
layer.scale = 0.12454696697215191
p1 = Path([[119, 281], [171, 177], [171, 11]],24)
p2 = Path([[42, 353], [29, 358], [29, 651], [48, 675]],249)
c7 = ClockAnimator(layer,[p1,p2])

# Clock 8
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [61, 247]
layer.scale = 0.08099471081759296
p1 = Path([[47, 214], [38, 192], [38, 8]],338)
c8 = ClockAnimator(layer,[p1])

# Clock 9
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [86, 189]
layer.scale = 0.053599212117783575
p1 = Path([[79, 168], [74, 156], [74, 10]],337)
c9 = ClockAnimator(layer,[p1])

# Clock 10
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [107, 150]
layer.scale = 0.04157799358572424
p1 = Path([[125, 145], [135, 142], [135, 10]],77)
p2 = Path([[102, 132], [100, 125], [100, 14]],344)
c10 = ClockAnimator(layer,[p1,p2])

# Clock 11
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [6, 226]
layer.scale = 0.04765220950975556
c11 = ClockAnimator(layer,[])

clocks_b = [c7,c8,c9,c10,c11]

# SET C =======================================================
# Clock 12
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [323, 249]
layer.scale = 0.13834804959451472
p1 = Path([[300, 191], [286, 162], [287, 8]],336)
c12 = ClockAnimator(layer,[p1])

# Clock 13
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [227, 208]
layer.scale = 0.08504444635847261
p1 = Path([[214, 174], [206, 149], [206, 9]],338)
c13 = ClockAnimator(layer,[p1])

# Clock 14
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [251, 155]
layer.scale = 0.045839737928260973
p1 = Path([[260, 139], [263, 132], [263, 7]],24)
c14 = ClockAnimator(layer,[p1])

# Clock 15
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [424, 288]
layer.scale = 0.1124036376923671
p1 = Path([[469, 304], [499, 315], [499, 356], [529, 376]],109)
c15 = ClockAnimator(layer,[p1])

# Clock 16
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [451, 217]
layer.scale = 0.056420223281877444
p1 = Path([[460, 194], [484, 140], [484, 11]],20)
c16 = ClockAnimator(layer,[p1])

# Clock 17
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [490, 202]
layer.scale = 0.03369641961943989
p1 = Path([[503, 197], [509, 194], [509, 10]],72)
p2 = Path([[494, 216], [508, 242], [508, 352], [537, 372]],163)
c17 = ClockAnimator(layer,[p1,p2])

# Clock 18
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [455, 350]
layer.scale = 0.03949909390643803
p1 = Path([[472, 356], [479, 358], [479, 406], [491, 414], [485, 417]],114)
p2 = Path([[462, 365], [466, 373], [466, 410], [475, 418]],160)
p3 = Path([[440, 357], [430, 362], [452, 385], [452, 416], [461, 424]],244)
c18 = ClockAnimator(layer,[p1,p2,p3])

# Clock 19
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [367, 152]
layer.scale = 0.09155346542316858
p1 = Path([[386, 117], [397, 95], [397, 10]],27)
c19 = ClockAnimator(layer,[p1])

# Clock 20
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [434, 132]
layer.scale = 0.06267216326897848
p1 = Path([[461, 125], [474, 121], [474, 9]],75)
c20 = ClockAnimator(layer,[p1])

# Clock 21
layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
layer.translation = [317, 126]
layer.scale = 0.032172258856130696
p1 = Path([[322, 113], [326, 106], [326, 6]],27)
c21 = ClockAnimator(layer,[p1])

clocks_c = [c12,c13,c14,c15,c16,c17,c18,c19,c20,c21]

# SET D =======================================================
# Clock 22
# Clock 23
# Clock 24
# Clock 25
# Clock 26

# SET E =======================================================
# Clock 27
# Clock 28
# Clock 29
# Clock 30
# Clock 31
# Clock 32
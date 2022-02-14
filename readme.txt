Instructions:

1. Run Python Scrubber.py to scrub poke mixer site for images and write hybridex.csv.  Images will automatically download into /images/%Type%/ based on the type of the suffix mon
2. manually populate /images/Backgrounds/%Type%/ with license free images
2.5 run SetBackground.py to combine background with mon png
3. Run Python AddImgToCard.py to attach mon to backgrounds by type and save output in /images/%Type%/output folder
4. move contents of output folders to /images/CardTemplates/%Type%
5. run Python AddFlareToCard.py to attach name, evolved from images (special case for eveelutions), rarity, height/weight
6. move contents of output folder to /images/CardsNoAbilities/%Type%
7. run Python ScrubForMoves.py to apply abilities, weakness, resist, retreat cost, and HP
from dymo_bluetooth import discover_printers, Canvas
import asyncio

async def main():
    # Canvas class allows constructing 1-bit images in ease.
    canvas = Canvas()

    # Pixels can be set and retrieved with methods.
    canvas.set_pixel(0, 0, True)

    # Images needs to be stretched by at least 2 times like
    # how its mobile app does, otherwise printer will render
    # the labels too narrow.
    canvas = canvas.stretch(2)

    # Get a list of printers.
    printers = await discover_printers()

    # Get the first discovered printer and print the 
    # constructed Canvas. Returns the print status.
    printer = printers[0]
    await printer.connect()
    await printer.print(canvas)

asyncio.run(main())
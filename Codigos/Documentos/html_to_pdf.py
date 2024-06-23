import asyncio
import os
from pyppeteer import launch


async def generate_pdf_from_html(html_path, output_path, semaphore):
    """
    Generates a PDF from the specified HTML file and saves it to the output path.

    Args:
        html_path (str): The path to the HTML file.
        output_path (str): The path to save the generated PDF.
        semaphore (asyncio.Semaphore): The semaphore to limit concurrent tasks.
    """

    async with semaphore:
        browser = await launch()
        page = await browser.newPage()

        try:
            # Load the HTML file using a more robust approach (consider error handling)
            await page.goto(f'file:///{os.path.abspath(html_path)}')

            # Generate the PDF with desired format and potential customizations
            await page.pdf({
                'path': output_path,
                'format': 'A4',  # Adjust format as needed (e.g., 'Letter')
                'margin': {  # Optional margin settings
                    'top': '2cm',
                    'right': '1cm',
                    'bottom': '2cm',
                    'left': '1cm'
                }
            })

        except Exception as e:
            print(f"Error generating PDF for {html_path}: {e}")  # Handle exceptions

        finally:
            await browser.close()


async def main(max_concurrent_tasks):
    html_files = [f for f in os.listdir("HTML") if f.endswith('.html')]
    tasks = []
    semaphore = asyncio.Semaphore(max_concurrent_tasks)

    for html_filename in html_files:
        html_path = os.path.join("HTML", html_filename)  # Assuming HTML files are in 'html_files' directory
        output_path = os.path.join("PDF", f"{html_filename.split('.')[0]}.pdf")  # Generate output path
        tasks.append(generate_pdf_from_html(html_path, output_path, semaphore))
    
    await asyncio.gather(*tasks)
    print("All PDF files generated!")

if __name__ == "__main__":
    max_concurrent_tasks = 10  # Adjust the number of concurrent tasks as needed
    asyncio.run(main(max_concurrent_tasks))


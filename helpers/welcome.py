from pyfiglet import Figlet
import click
# helper function to render modules and functions - starting up cli
def render(text, f):
    print(f.renderText(text))

f=Figlet(font='straight')
render('-----------------', f)
f=Figlet(font='big')
render('🪣 BucketGalaxy CLI 🪣',f)
# render('A python client for digitalocean postgres clusters\n-----------------\n', f)
f=Figlet(font='straight')
render('-----------------\n', f)
click.echo(click.style('Welcome to BucketGalaxy,', bold=True, fg='white', bg='green'))
click.echo(click.style('the unofficial s3 CLI across cloud providers (AWS, GCP, Azure, DigitalOcean).\n\n', fg='white', italic=True))
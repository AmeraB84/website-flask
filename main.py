from distutils.log import debug
from website import create_app

app = create_app()

if __name__ == '__main__': # excute this line if we execute this file not if we import it 
    app.run(debug=True)
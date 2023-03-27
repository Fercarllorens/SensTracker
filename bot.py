import discord
from discord.ext import commands
from funcionalities.generateWC import wordcloudsimple
from funcionalities.vsprofiles import vsprofiles
from funcionalities.analysemovie import analyseMovie
from funcionalities.analyseprofile import analyseprofile


def run_discord_bot():
    TOKEN = 'MTA4ODIyNzg5NTQwMDQ4MDg0MA.GQx_Lb.my8UeeEQI4jHb2Tveq3x1PO43jfIetbzVdYx_U'
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(intents=intents, command_prefix='!')

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(name="!help"))
        print(f'{client.user} is now running!')

    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Comando no existente. Utilice **!help** para obtener el listado de comandos disponibles.")


    @client.command(brief="Comparación de dos usuarios en Twitter", 
                    description="Genera una gráfica comparando los estados de felicidad entre dos usuarios en Twitter. No es necesario poner el @ del nick. Por ejemplo: !versus Usuario1 Usuario2")
    async def versus(ctx, usuario1, usuario2):
        await ctx.send("Realizando la comparativa entre los usuarios @" + usuario1 + " y @" + usuario2 + "\n**NOTA:** limitado a tweets de la última semana")
        fileName = vsprofiles(usuario1, usuario2)
        if fileName != "":
            with open(fileName, 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)
    
    @versus.error
    async def command_error(ctx, error):
        await ctx.send('Error')
        await ctx.send('Se necesitan 2 argumentos en la función versus. Por ejemplo: !versus usuario1 usuario2')


    @client.command(brief="Muestra a los autores del bot.",
                    description="Muestra a los autores del bot.")
    async def about(ctx):
        await ctx.send("Proyecto creado por: **Angel Romero** y **Fernando Carceller**.\nProgramado para la asignatura ERS del máster MUITSS.")


    @client.command(brief="Publica WordCloud de un usuario de Twitter.",
                    description="Genera un WordCloud del usuario que se indica en el argumento.")
    async def wordcloud(ctx, usuario):
        await ctx.send("Generando el WordCloud del usuario @" + str.lower(usuario))
        file = wordcloudsimple(usuario)
        with open(file, 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
        
    
    @client.command()
    async def movie(ctx, *args):
        movie = ' '.join(args)

        await ctx.send("Generando el análisis de la película " + movie)
        files = analyseMovie(movie)
        link = files.pop()
        await ctx.send("Para más información, visitar el siguiente link: " + link)
        for file in files:
            with open(file, 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)


    @movie.error
    async def movie_error(ctx, error):
        await ctx.send("Error procesando la solicitud. Reinténtelo más adelante o pruebe con otra película.")

    @client.command()
    async def profile(ctx, user):
        await ctx.send("Generando el análisis para el usuario @" + user)
        files = analyseprofile(user)
        for file in files:
            try:
                with open(file, 'rb') as f:
                    picture = discord.File(f)
                    await ctx.send(file=picture)
            except:
                pass

    @profile.error
    async def movie_error(ctx, error):
        await ctx.send("Error procesando la solicitud. Reinténtelo más adelante o pruebe con otro usuario.")
        await ctx.send(error)

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)

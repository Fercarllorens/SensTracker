import discord
from discord.ext import commands
from funcionalities.generateWC import wordcloudsimple
from funcionalities.vsprofiles import vsprofiles
from funcionalities.analysemovie import analyseMovie
from funcionalities.analyseprofile import analyseprofile


def run_discord_bot():
    TOKEN = 'X'
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
        
    
    @client.command(brief="Publica un enlace con la película y un análisis de sentimientos sobre ella.",
                    description="")
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
        await ctx.send(error)

    @client.command(brief="Realiza un análisis de sentimientos sobre los últimos tweets publicados y noticias relacionadas con él.",
                    description="Realiza un análisis de sentimientos sobre los últimos tweets publicados y noticias relacionadas con él.")
    async def profile(ctx, user, *realname):
        try:
            realname = ' '.join(realname)
        except:
            realname = ""
        await ctx.send("Generando el análisis para el usuario @" + user)
        if realname == "":
            files = analyseprofile(user, user)
        else:
            files = analyseprofile(user, realname)
        news = files.pop()
        for file in files:
            try:
                with open(file, 'rb') as f:
                    picture = discord.File(f)
                    await ctx.send(file=picture)
            except:
                pass
        if realname == "":
            await ctx.send("**WARNING**: no se ha especificado el nombre real del usuario. Las noticias mostradas podrían no ser las reales o no mostrar resultados.\n"
                           + "Utilice el comando: !profile usuariotwitter Nombre Apellido")
            realName = user

        await ctx.send("Últimas noticias relacionadas con " + realname)
        for link in news:
            await ctx.send(link[0] + ": " + link[1])

    @profile.error
    async def movie_error(ctx, error):
        await ctx.send("Error procesando la solicitud. Reinténtelo más adelante o pruebe con otro usuario.\nDebe ser un usuario con al menos un tweet en la última semana. Compruebe que sea un usuario activo")

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)

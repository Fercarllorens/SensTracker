import discord
import responses
from discord.ext import commands
from funcionalities.generateWC import wordcloudsimple
from funcionalities.vsprofiles import vsprofiles


# Send messages
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


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
        
    


    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)

    
#Utilidades de debugging de mensajes y contenidos de usuarios
'''@client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == client.user:
            return

        # Get data about the user
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")
        
        # If the user message contains a '?' in front of the text, it becomes a private message
        if user_message[0] == '?':
            user_message = user_message[1:]  # [1:] Removes the '?'
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
        
        await send_message(message, user_message, is_private=False)
        '''
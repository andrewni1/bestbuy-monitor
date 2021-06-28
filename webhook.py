from discord_webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/858703915255595038/cPuYpwCHH0B3RTTjf3RNy9GajYOZocf46mr7gr_cURkR3JNKNsKiADqsQvM2exx38CLD', username="BestBuy")

def sendAlert(productURL, productName, price, sku, imageURL, ATC):
    embed = DiscordEmbed(title=productName, url=productURL, color='03b2f8')
    embed.set_timestamp()
    embed.add_embed_field(name='SKU', value=sku)
    embed.add_embed_field(name='Price', value=price)
    embed.add_embed_field(name='Add to cart', value=ATC, inline=False)
    embed.set_thumbnail(url=imageURL)

    webhook.add_embed(embed)
    response = webhook.execute()
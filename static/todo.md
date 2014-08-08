###Todo
- User signs up, database stores:
    - id, email, minecraft username
            def create_server(minecraft_username, server_image, email, time):
                server_image = minecraft_image
                email = server_name
                time = time in hours
                # we'll create a cronjob later on to cycle through and delete a server after it's alotted time.
                # however, before deleting a server, we'll send an email stating what's about to happen and give
                # them time to renew

                # we'll use this digital ocean python api https://github.com/ahmontero/dop
                # there are good examples on there about how to shutdown droplets

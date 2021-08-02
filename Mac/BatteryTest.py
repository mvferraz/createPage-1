import datetime
import os
import sched
import time

import psycopg2

# import Environment
# import SendMessage
# import FacebookMessage

s = sched.scheduler(time.time, time.sleep)

BATTERY_LIMIT = 20


# Checks the battery level and notifies user
def check_battery_level(sc):

    try:
        try:
            print("Connecting to Database")
            # Connecting to postgres database
            conn = psycopg2.connect(
                host=os.environ.get('POSTGRES_DB_HOST'),
                database=os.environ.get('POSTGRES_DB_DATABASE'),
                user=os.environ.get('POSTGRES_DB_USER'),
                password=os.environ.get('POSTGRES_DB_PASSWORD')
            )
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
            print('Database is not reachable. Check your internet connection. We will try again in 1 minute.')
        else:
            print('connected')

            cur = conn.cursor()

            # Gets battery level from console
            print("Getting battery level...")
            battery_level = str(os.popen('pmset -g batt').read().split(";")[0].split('\t')[1])

            battery_log = "{1} - Battery level is {0}\n".format(battery_level, datetime.datetime.now())
            print(battery_log)

            # Retrieving info from database
            select_command = 'select * from public.device_status where id = 1'

            print('Executing Select Command')

            cur.execute(select_command)
            print('Fetching records')
            records = cur.fetchall()

            database_battery_level = records[0][2]
            print('Got records from database: {0}'.format(database_battery_level))

            # if int(battery_level.replace("%", "")) > 80:
                # FacebookMessage.send_whats_message("Battery is {0}".format(battery_level))


            # Sends warning Whatsapp message in case battery level is too low
            if int(battery_level.replace("%", "")) <= BATTERY_LIMIT:
                warning_message = 'Your battery level is too low ({0}), you may want to recharge it now.'\
                    .format(battery_level)
                print(warning_message)
                # SendMessage.send_whats_message(warning_message)
                # FacebookMessage.send_whats_message(warning_message)

            # If battery level does not match with database, it will update database and message user on Whatsapp
            if database_battery_level != battery_level:

                # Logs battery level
                try:
                    f = open("/Users/marcusferraz/Documents/Angular/portfolio/PythonTest/Sa.txt", "a")
                    f.write(battery_log)
                except:
                    f.close()

                update_message = "Computer Battery ({0}) does not match with recorded value ({1}). Hold on, " \
                                  "we are updating database...".format(battery_level, database_battery_level)

                print(update_message)

                # Updates database
                cur.execute("UPDATE public.device_status SET battery = '{0}' where id = 1".format(battery_level))
                conn.commit()
        finally:
            print("Closing connection to Database")
            cur.close()
            conn.close()

    except Exception as e:
        print("Oops!", e.__class__, "occurred.")

    finally:
        print('Cycle ended')
        print('--------------------------------------\n\n')

    # Run after 5 seconds
    s.enter(60, 1, check_battery_level, (sc,))


# Run after 1 second
s.enter(1, 1, check_battery_level, (s,))
s.run()

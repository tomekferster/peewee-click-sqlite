import click
import re
import string
from datetime import date, datetime
from main import (
                Dob,
                Location, 
                Login,
                Name,
                Person
)
           


@click.group()
def cli():
    pass


@cli.command()
@click.option('--gender',
              type=click.Choice(['all', 'female', 'male'], case_sensitive=False),
              help="Specify gender", default='all', show_default=True)
def average_age(gender):
    """
    Specify gender to get the average age
    """
    count_all = 0
    age_all = 0

    if gender == 'female' or gender == 'male':
        dobs = Dob.select().join(Person).where(Person.gender == gender)
    else:
        dobs = Dob.select()
    
    for dob in dobs:
        age_all += dob.age
    count_all = dobs.count()
    click.echo("Average age for {} is {:.1f} years".format(gender, age_all/count_all))


@cli.command()
@click.argument('number', default=1)
def most_common_cities(number):
    """
    Specify the number to get the most common cities
    """
    city_count = {}

    locations = Location.select()
    for location in locations:
        if location.city in city_count.keys():
            city_count[location.city] += 1
        else:
            city_count[location.city] = 1

    most_popular = sorted(city_count.items(), key=lambda x: x[1], reverse=True)
    
    if number > locations.count():
        print("You exceeded the maximum number of records available. The maximum will be displayed:")
        number = locations.count()

    for index in range(number):
        city, count = most_popular[index]
        click.echo("{} - {}".format(city, count))


@cli.command()
@click.argument('number', default=1)
def most_common_passwords(number):
    """
    Specify the number to get the most common passwords
    """
    password_count = {}

    logins = Login.select()
    for login in logins:
        if login.password in password_count.keys():
            password_count[login.password] += 1
        else:
            password_count[login.password] = 1

    most_popular = sorted(password_count.items(), key=lambda x: x[1], reverse=True)

    if number > logins.count():
        print("You exceeded the maximum number of records available. The maximum will be displayed:")
        number = logins.count()

    for index in range(number):
        password, count = most_popular[index]
        click.echo("{} - {}".format(password, count))


@cli.command()
def most_secure_password():
    """
    Get the best rated password
    """
    best_score = 0
    best_password = ''
    special_chars = set(string.punctuation.replace("_", ""))
    
    logins = Login.select()
    for login in logins:
        score = 0
        password = login.password
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 2
        if re.search(r'[1-9]', password):
            score += 1
        if len(password) > 7:
            score += 5
        if any(char in special_chars for char in password):
            score += 3
        
        if score > best_score:
            best_score = score
            best_password = password
    click.echo("Best password: {}, score: {}".format(best_password, best_score))


def get_date(date_input):
    """
    Function for dates evaluation, it returns 'date' type, if given correctly.
    Used only by 'people_by_dob_range' cli command
    """
    while True:
        try:
            dt = date(int(date_input[:4]), int(date_input[5:7]), int(date_input[8:10]))
            break
        except:
            print("Wrong value, remember about the right format! (YYYY-MM-DD)")
            date_input = input("Provide the date (YYYY-MM-DD): ")
            continue
    return dt

@cli.command()
def people_by_dob_range():
    """
    Provide the date range and get all the people within this range
    """
    flag_change = ''
    flag_found = False
    date1 = click.prompt("Provide the first date (YYYY-MM-DD)", value_proc=get_date)
    date2 = click.prompt("Provide the second date (YYYY-MM-DD)", value_proc=get_date)

    # if the first date is greater than the second one, change the places of these dates
    if date1 > date2:
        flag_change = date2
        date2 = date1
        date1 = flag_change
    
    persons = Person.select()
    for person in persons:
        dob = Dob.select().join(Person).where(Person.id == person.id).get()
        name = Name.select().join(Person).where(Person.id == person.id).get()
        dt = datetime.strptime(dob.date, "%Y-%m-%dT%H:%M:%S.%fZ")
        dob_new = date(dt.year, dt.month, dt.day)

        if date1 <= dob_new <= date2:
            result = name.first + ' ' + name.last + ' - ' + str(dob_new)
            click.echo(result)
            flag_found = True
    if not flag_found:
        click.echo("No results!")


@cli.command()
@click.option('--gender',
              type=click.Choice(['female', 'male'], case_sensitive=False), 
              help="Specify gender", required=True)
def percent_by_gender(gender):
    """
    Get the percentage of the specified gender in the whole community
    """
    count_all = 0
    count_choice = 0

    if gender == 'female' or gender == 'male':
        count_all = Person.select().count()
        count_choice = Person.select().where(Person.gender == gender).count()
        click.echo('Percent of {}: {:.1f}%'.format(gender, count_choice * 100/count_all))
    else:
        click.echo('Wrong gender, try again!')
        

if __name__ == "__main__":
    cli()
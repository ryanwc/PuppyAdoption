# AdoptAPuppy

AdoptAPuppy is a database that manages puppy adoptions.

# Tables in the Database

- Puppy
	- puppies with biographical info
- Shelter
	- shelters with address and capacity
- Adopter
	- unique records matching a puppy to its adopter (if applicable)
- Person
	- adopters with link to household
- Household
	- households with address

# Interesting Features

## Load Balancing

The provided addPuppyToShelter() automatically adds a new puppy to the shelter that is the least full regardless of which shelter is specified by the user (and notifies the user 1) that it made the switch and 2) why it made the switch).  The same method also rejects a new puppy (fails to add to the database and prints a related message) if every shelter is at capacity.

# Technologies Used

- Python 2.7
- SQLAlchemy 1.1
- SQLite

# License

This software is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl.html). Accordingly, you are free to run, study, share, and modify this software only if you give these same freedoms to users of your implementation of this software.
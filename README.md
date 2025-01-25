# atproto-auto-blocklist

This is a script that allows you to automatically generate a blocklist (AKA moderation list) for Bluesky based on a query.

## Usage

1. Clone this repository: `git clone https://github.com/ndri/atproto-auto-blocklist.git`
2. Change into the directory: `cd atproto-auto-blocklist`
3. Create a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/): `python3 -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install the dependencies: `pip install -r requirements.txt`
6. Configure the environment variables (see below).
7. Run the script: `python3 add_to_blocklist.py`

## Configuration

You can configure the script with command line arguments, environment variables or the `.env` file.

To run this script, you need to set your Bluesky login credentials, the ID of the blocklist to add users to, the search term to find users with and the query to filter the found users.

The reason there is both a search term and a query is that the AT Protocol only allows you to search users with a simple text query that finds users based on their name, handle or bio and it can return some users that you don't want to block. The query is used to filter out those users.

### Environment variables

See the `.env.example` file for a list of environment variables that you can set.

### .env file

Make a copy of the `.env.example` file and name it `.env`:

```bash
cp .env.example .env
```

Fill in the values for the environment variables:

- `USERNAME` - Your Bluesky username.
- `PASSWORD` - A Bluesky [app password](https://bsky.app/settings/app-passwords).
- `BLOCKLIST_ID` - The ID of the blocklist to add users to, i.e. `https://bsky.app/profile/<handle>/lists/<this-part>`.
- `SEARCH_TERM` - The search term to find users with. Note that this will find many users that don't exactly match the search term.
- `QUERY` - A Lucene query to filter the found users with.
- `QUIET` (optional) - If set to `true`, the script will not print any output.
- `DRY_RUN` (optional) - If set to `true`, the script will not add any users to the blocklist, only output the users that would be added.

### Command line arguments

Command line arguments take precedence over environment variables.

```
options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Your ATProto username
  -p PASSWORD, --password PASSWORD
                        Your ATProto app password. Generate one at https://bsky.app/settings/app-passwords.
  -l LIST_ID, --list-id LIST_ID
                        The ID of the blocklist to add users to, i.e. https://bsky.app/profile/<handle>/lists/<this-part>.
  -s SEARCH_TERM, --search-term SEARCH_TERM
                        The term to search AT Protocol users for.
  -q QUERY, --query QUERY
                        A Lucene query to filter the found users with. Necessary because the search term will find users that don't exactly match the search term.
  -d, --dry-run         Whether to actually add users to the blocklist.
  -x, --quiet           Whether to suppress output. Useful if running as a cron job.
```

## Querying

This script lets you use a [Lucene query](https://lucene.apache.org/core/3_6_0/queryparsersyntax.html) using [Luqum](https://luqum.readthedocs.io/en/latest/about.html) to precisely match which users you want to add to the blocklist. Note that not all Lucene features are supported.

- You can query these fields: `handle`, `display_name` and `description`.
- You can use negative queries to exclude certain values, e.g. `-handle:example`.
- You can use `AND`, `OR` and `NOT` operators.
- You can use parentheses to group queries.
- You can use regular expressions using `/` and `/` as delimiters.

You can use the `--dry-run` flag or `DRY_RUN=true` environment values to see which users would be added to the blocklist without actually adding them. Maybe you'll find users who would be added, but for whom you should add a negative part to the query.

### Examples

- `handle:example` - Match users that have `example` in their handle.
- `handle:example AND -display_name:example` - Match users that have `example` in their handle but not in their display name.
- `handle:/^example/` - Match users that have a handle that starts with `example`.
- `handle:/example$/` - Match users that have a handle that ends with `example`.
- `handle:/example/ OR handle:/test/` - Match users that have a handle that contains `example` or `test`.
- `handle:/example/ AND NOT handle:/test/` - Match users that have a handle that contains `example` but not `test`.
- `handle:example AND (display_name:example OR description:example)` - Match users that have a handle that contains `example` and have `example` in their display name or description.
- `description:hater AND -description:/anti[- ]hater/` - Match users that have `hater` in their description but not `anti-hater` or `anti hater`.

See `utils/test_dict_matcher.py` for some more examples.

## Example blocklists

These are some example blocklists that are generated using this script. Feel free to add yours here.

### e/acc

- Link: https://bsky.app/profile/andri.io/lists/3lben4phiyh26
- Search term: `e/acc`
- Query: `display_name:e/acc AND -display_name:/(anti[- ]e\/acc)/ OR description:e/acc AND -description:/(anti[- ]e\/acc)/`
- Full command: `python3 add_to_blocklist.py -l 3lben4phiyh26 -s e/acc -q "display_name:e/acc AND -display_name:/(anti[- ]e\/acc)/ OR description:e/acc AND -description:/(anti[- ]e\/acc)/"`

## Notes

- This script does not automatically update the list. Run it regularly or set up a [cron job](https://askubuntu.com/questions/2368/how-do-i-set-up-a-cron-job) to do so.
- This script does not remove users from the blocklist if they no longer match the query. This might be added in the future.
- If you block the users in the blocklist, they will not show up in the search results anymore.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Fix Database Permissions

## Issue
The `saferoute_user` doesn't have permission to create tables in the `public` schema.

## Solution

You need to grant permissions to the user. Here are the steps:

### Option 1: Using pgAdmin (Easiest)

1. **Open pgAdmin**
2. **Connect to your PostgreSQL server** (as postgres user)
3. **Right-click on `saferoute_db`** → **Query Tool**
4. **Paste and run this SQL**:

```sql
-- Grant schema usage
GRANT USAGE ON SCHEMA public TO saferoute_user;

-- Grant create privileges
GRANT CREATE ON SCHEMA public TO saferoute_user;

-- Grant all privileges on database
GRANT ALL PRIVILEGES ON DATABASE saferoute_db TO saferoute_user;

-- Grant all privileges on all tables (for existing and future tables)
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO saferoute_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO saferoute_user;

-- If tables already exist, grant privileges on them
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO saferoute_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO saferoute_user;
```

5. **Click Execute** (or press F5)

### Option 2: Using psql (Command Line)

If you can access psql:

```powershell
# Connect as postgres user
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d saferoute_db

# Then run the SQL commands above
```

### Option 3: Use postgres user directly (Quick Fix)

If you want to use the `postgres` user instead of `saferoute_user`, update `saferoute/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'saferoute_db',
        'USER': 'postgres',  # Changed from saferoute_user
        'PASSWORD': 'your_postgres_password',  # Your postgres password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Note:** Using the postgres superuser is fine for development but not recommended for production.

## After Fixing Permissions

Run migrations again:
```powershell
python manage.py migrate
```

Then create a superuser:
```powershell
python manage.py createsuperuser
```


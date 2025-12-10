# Checking PostgreSQL Installation

## Issue: `psql` command not found

This means PostgreSQL might not be installed, or it's not in your system PATH.

## Step 1: Check if PostgreSQL is Installed

### Option A: Check via Windows Services
1. Press `Win + R`, type `services.msc`, press Enter
2. Look for "postgresql" services
3. If you see services like "postgresql-x64-XX", PostgreSQL is installed

### Option B: Check Installation Directory
PostgreSQL is usually installed in:
- `C:\Program Files\PostgreSQL\XX\` (where XX is version number)
- Look for `bin\psql.exe` in that directory

## Step 2: If PostgreSQL is NOT Installed

1. **Download PostgreSQL** from: https://www.postgresql.org/download/windows/
2. **Run the installer** and follow the setup wizard
3. **Remember the password** you set for the `postgres` user
4. **Add to PATH** (optional but recommended):
   - During installation, check "Add PostgreSQL bin directory to PATH"
   - Or manually add: `C:\Program Files\PostgreSQL\XX\bin` to your system PATH

## Step 3: If PostgreSQL IS Installed (but psql not in PATH)

### Method 1: Use Full Path
```powershell
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres
```
(Replace `15` with your PostgreSQL version number)

### Method 2: Add to PATH Temporarily (Current Session)
```powershell
$env:Path += ";C:\Program Files\PostgreSQL\15\bin"
psql -U postgres
```

### Method 3: Use pgAdmin (GUI)
1. Open **pgAdmin** (usually in Start Menu)
2. Connect to your PostgreSQL server
3. Right-click "Databases" → Create → Database
4. Name: `saferoute_db`

## Step 4: Create Database Using pgAdmin (Easiest Method)

1. **Open pgAdmin** (search in Start Menu)
2. **Connect** to your PostgreSQL server (enter your postgres password)
3. **Right-click on "Databases"** → **Create** → **Database**
4. **Enter:**
   - Database name: `saferoute_db`
   - Owner: `postgres` (or create a new user)
5. **Click "Save"**

## Step 5: Create Database User (Optional but Recommended)

In pgAdmin:
1. **Right-click "Login/Group Roles"** → **Create** → **Login/Group Role**
2. **General tab:**
   - Name: `saferoute_user`
3. **Definition tab:**
   - Password: `$Moses23` (or your preferred password)
4. **Privileges tab:**
   - Check "Can login?"
   - Check "Create databases?"
5. **Click "Save"**

## Step 6: Update settings.py

Your `saferoute/settings.py` already has:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'saferoute_db',
        'USER': 'saferoute_user',
        'PASSWORD': '$Moses23',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**If you used the default `postgres` user instead**, change:
```python
'USER': 'postgres',
'PASSWORD': 'your_postgres_password',  # The password you set during installation
```

## Step 7: Test Connection

After creating the database, run:
```powershell
python test_db_connection.py
```

This will verify your database connection is working.


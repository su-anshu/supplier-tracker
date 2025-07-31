# AWS EC2 Deployment Guide
## Mithila Foods Supplier Tracker System

### Prerequisites
- AWS EC2 instance (Ubuntu 20.04 LTS or later)
- Security Group allowing HTTP (80) and HTTPS (443) traffic
- SSH access to the instance

### Quick Deployment Steps

#### 1. Connect to your EC2 instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

#### 2. Clone/Upload your project
```bash
# Option A: If using git
git clone your-repository-url supplier_tracker
cd supplier_tracker

# Option B: If uploading files
# Upload your project files to /home/ubuntu/supplier_tracker/
```

#### 3. Make deployment script executable and run
```bash
chmod +x deploy_aws.sh
./deploy_aws.sh
```

#### 4. Configure environment variables
```bash
# Edit the .env file with your production values
nano .env

# Set these critical values:
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-ec2-ip
```

#### 5. Create admin user (optional)
```bash
source venv/bin/activate
python manage.py createsuperuser
```

#### 6. Test the application
Visit `http://your-ec2-public-ip/` in your browser

### Environment Variables for Production

Create/update `.env` file with:
```env
# Django Settings
SECRET_KEY=your-super-secret-production-key-change-this
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-ec2-ip,localhost

# Database: SQLite (default - no additional config needed)
# Your db.sqlite3 file will be used automatically

# Optional: PostgreSQL (if you upgrade later)
# DB_NAME=your_database_name
# DB_USER=your_database_user
# DB_PASSWORD=your_database_password
# DB_HOST=your_database_host
# DB_PORT=5432

# AWS Settings (if using S3)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_STORAGE_BUCKET_NAME=your_s3_bucket

# Email Settings (if needed)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=noreply@yourcompany.com

# Company Information
COMPANY_NAME=Mithila Foods
```

### Troubleshooting

#### If deployment fails:
1. Check logs: `sudo journalctl -u supplier-tracker`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Test manually: `python manage.py runserver 0.0.0.0:8000`

#### Common issues:
- **Port already in use**: Stop other services or change port
- **Permission denied**: Check file permissions and ownership
- **Database errors**: Ensure database is properly configured
- **Static files not loading**: Run `python manage.py collectstatic`

#### Service management:
```bash
# Restart application
sudo systemctl restart supplier-tracker

# Restart web server
sudo systemctl restart nginx

# Check status
sudo systemctl status supplier-tracker
sudo systemctl status nginx
```

### Security Checklist
- [ ] Changed default SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configured proper ALLOWED_HOSTS
- [ ] Set up SSL certificate (recommended)
- [ ] Configure firewall/Security Groups
- [ ] Regular backups configured (especially db.sqlite3 file)

### SQLite Database Management
```bash
# Backup database
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Check database size
ls -lh db.sqlite3

# SQLite command line access
sqlite3 db.sqlite3
```

### Performance Optimization
- [ ] Configure database connection pooling
- [ ] Set up Redis for caching
- [ ] Configure static file CDN
- [ ] Monitor resource usage
- [ ] Set up log rotation

### Support
If you encounter issues:
1. Check the deployment logs
2. Verify all environment variables are set
3. Ensure EC2 security groups allow required traffic
4. Test database connectivity

The deployment script handles most common setup tasks automatically. For custom requirements, modify the script accordingly.

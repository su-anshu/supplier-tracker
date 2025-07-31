# AWS EC2 Deployment Checklist
## Pre-Deployment Quick Check

### ✅ Critical Files Updated
- [x] `requirements.txt` - Added psycopg2-binary
- [x] `settings.py` - AWS EC2 compatible configurations
- [x] `.env.example` - Production environment template
- [x] `deploy_aws.sh` - Automated deployment script
- [x] `AWS_DEPLOYMENT_GUIDE.md` - Step-by-step instructions

### 🚀 Deployment Steps

#### 1. Prepare EC2 Instance
- [ ] Launch Ubuntu 20.04+ instance
- [ ] Configure Security Group (ports 22, 80, 443)
- [ ] Note down public IP address

#### 2. Upload Project Files
- [ ] Upload all project files to `/home/ubuntu/supplier_tracker/`
- [ ] Or clone from repository

#### 3. Run Deployment
```bash
cd supplier_tracker
chmod +x deploy_aws.sh
./deploy_aws.sh
```

#### 4. Configure Production Settings
- [ ] Copy `.env.example` to `.env`
- [ ] Update `SECRET_KEY` with strong value
- [ ] Set `DEBUG=False`
- [ ] Update `ALLOWED_HOSTS` with your domain/IP

#### 5. Final Steps
- [ ] Create admin user: `python manage.py createsuperuser`
- [ ] Test application: `http://your-ec2-ip/`
- [ ] Test admin panel: `http://your-ec2-ip/admin/`

### 🔧 Post-Deployment

#### Optional Enhancements
- [ ] Set up SSL certificate (Let's Encrypt)
- [ ] Configure custom domain
- [ ] Set up database backups
- [ ] Configure monitoring

#### Service Commands
```bash
# Restart application
sudo systemctl restart supplier-tracker

# View logs
sudo journalctl -u supplier-tracker -f

# Restart web server
sudo systemctl restart nginx
```

### 🆘 Troubleshooting

#### If application doesn't start:
1. Check service logs: `sudo journalctl -u supplier-tracker`
2. Check environment variables in `.env`
3. Test manually: `python manage.py runserver 0.0.0.0:8000`

#### If static files don't load:
1. Run: `python manage.py collectstatic`
2. Check Nginx configuration
3. Verify file permissions

### 📝 Notes
- The deployment script handles most setup automatically
- Database uses SQLite (perfect for small to medium applications)
- Your existing db.sqlite3 file will be used in production
- Can upgrade to PostgreSQL later if needed (high traffic scenarios)
- All critical deployment blockers have been fixed

### 🎯 Success Criteria
- [ ] Application loads at `http://your-ec2-ip/`
- [ ] Admin panel accessible at `http://your-ec2-ip/admin/`
- [ ] Static files (CSS/JS) loading properly
- [ ] No server errors in logs
- [ ] Can create/edit items through the interface

**Your application is now deployment-ready for AWS EC2!** 🚀

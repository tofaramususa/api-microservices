docker run -d \
  -p 8000:8000 \
  -e DOMAIN="example.com" \
  -e SMTP_HOST="smtp.example.com" \
  my-fastapi-app
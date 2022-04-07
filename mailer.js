const mailer = require('nodemailer');
const fs = require('fs');
require('dotenv').config();

const transport = mailer.createTransport({
  host: 'smtp.gmail.com',
  port: 465,
  secure: true,
  auth: {
    user: process.env.USERNAME,
    pass: process.env.PASSWORD
  }
});

const data = fs.readFileSync('./lastchance.txt', 'utf8').trim();

if (data.length > 0) {
  transport.sendMail({
    from: process.env.USERNAME,
    to: process.env.TARGET,
    subject: 'Found last chance products!',
    text: `${data}\n`
  }, (err, info) => {
    if (err) {
      console.error(err);
    } else {
      console.log(info);
    }
  });
}

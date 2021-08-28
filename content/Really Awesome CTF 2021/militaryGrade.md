Title: Military Grade
Date: 2021-08-15

We are presented with a simple webservice written in go which randomly changes the encryption key every 672 ms and outputs the encrypted flag. However if we analyze the seed that is used to initialize the random number generator ...

    :::go
    func changer() {
        ticker := time.NewTicker(time.Millisecond * 672).C
        for range ticker {
            rand.Seed(time.Now().UnixNano() & ^0x7FFFFFFFFEFFF000)

            ...
        }
    }

... we find out that there are only 13 bits that are chosen randomly in the changer() function.

    :::
    ^0x7FFFFFFFFEFFF000
    -> ^0111 1111 1111 1111 1111 1111 1111 1111 1111 1110 1111 1111 1111 0000 0000 0000
    ->  1000 0000 0000 0000 0000 0000 0000 0000 0000 0001 0000 0000 0000 1111 1111 1111
        ^                                               ^                ^
        63 th bit - sign                                |                |
                                                        24 th bit        |
                                                                         12 bit number

So we can simply bruteforce all possible seeds to create "random" encryption keys the same way as the main.go file until the output of the webservice decodes to something that starts with "ractf{".

    :::go
    package main
    
    import (
        "bytes"
        "crypto/aes"
        "crypto/cipher"
        "encoding/hex"
        "fmt"
        "log"
        "math/rand"
        "net/http"
        "os"
        "strings"
        "sync"
        "time"
    )
    
    const rawFlag = "[REDACTED]"
    
    var flag string
    var flagmu sync.Mutex
    
    func decrypt(ciphertextHex string, bKey []byte, blockSize int) string {
        ciphertext, err := hex.DecodeString(ciphertextHex)
        if err != nil {
            log.Println(err)
            return ""
        }
    
        bIV := []byte(ciphertext)[:blockSize]
        bCiphertext := []byte(ciphertext)[blockSize:]
        block, err := aes.NewCipher(bKey)
        if err != nil {
            log.Println(err)
            return ""
        }
    
        plaintext := make([]byte, len(bCiphertext))
        mode := cipher.NewCBCDecrypter(block, bIV)
        mode.CryptBlocks(plaintext, bCiphertext)
        return string(plaintext)
    }
    
    func main() {
        var key []byte
        var iv []byte
    
        for i := 0; i < 32; i++ {
            key = append(key, byte(1))
        }
    
        for i := 0; i < aes.BlockSize; i++ {
            iv = append(iv, byte(1))
        }
    
        if len(os.Args) <= 1 {
            log.Println("No ciphertext given -> Ending now")
            return
        }
    
        ciphertextWithoutIV := os.Args[1]
        log.Println("Decrypting "+ ciphertextWithoutIV)
    
        // iterate twice over the 12 bit number range
        // first with bit 24 set to 0
        // second with bit 24 set to 1
        for flipBit24 := 0; flipBit24 < 2; flipBit24++ {
            for j := 0; j < (1<<12); j++ {
                seed := int64(j);
                if flipBit24 != 0 {
                    seed |= int64(1)<<24
                }
    
                rand.Seed(seed)
                for k := 0; k < rand.Intn(32); k++ {
                    rand.Seed(rand.Int63())
                }
    
                var key []byte
                var iv []byte
    
                for k := 0; k < 32; k++ {
                    key = append(key, byte(rand.Intn(255)))
                }
    
                for k := 0; k < aes.BlockSize; k++ {
                    iv = append(iv, byte(rand.Intn(255)))
                }
    
                ciphertext = hex.EncodeToString(iv) + ciphertextWithoutIV
    
                plaintext = decrypt(ciphertext, key, aes.BlockSize)
    
                if strings.Index(plaintext, "ractf{") == 0 || strings.Index(plaintext, "[REDACTED]") == 0 {
                    print(plaintext)
                }
            }
        }
    }


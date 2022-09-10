# Changelog

<!--next-version-placeholder-->

## v0.6.8 (2022-09-10)
### Fix
* Add partition GUID for Linux, Windows, Mac ([`e45c102`](https://github.com/swysocki/gpt-image/commit/e45c10221e952a84967b254962b9a6d0b75490a3))

## v0.6.7 (2022-08-09)
### Fix
* Raise an error if partition is too large ([`f4b1fca`](https://github.com/swysocki/gpt-image/commit/f4b1fcae926d1ce32f2c5fa415fcb4404d268cba))

## v0.6.6 (2022-08-02)
### Fix
* Ensure disk GUID's match in header ([`5b7503f`](https://github.com/swysocki/gpt-image/commit/5b7503fd9bab243958d6dc2470d4a9b255d5084f))

### Documentation
* Update quick start example ([`d28dd28`](https://github.com/swysocki/gpt-image/commit/d28dd281f94cced2ce32350eb0f560fe079fc408))

## v0.6.5 (2022-07-31)
### Fix
* Add types tests to CI ([`fee4da6`](https://github.com/swysocki/gpt-image/commit/fee4da6d99392c69a5efffdbb8c09324e93eab07))

## v0.6.4 (2022-07-28)
### Fix
* Make attributes integer-like ([`1f875cb`](https://github.com/swysocki/gpt-image/commit/1f875cbbf1d0ec973957747b8653fd4445d2d10a))

### Documentation
* Denote partition UUID in creation step ([`8f768d7`](https://github.com/swysocki/gpt-image/commit/8f768d758eeb1f735f94432adf555b6c927b6ce6))

## v0.6.3 (2022-07-27)
### Fix
* Add py.typed to package ([`3b13b41`](https://github.com/swysocki/gpt-image/commit/3b13b41bdcfd3a6d1733264a1d8fd4d90329f388))

## v0.6.2 (2022-07-25)
### Fix
* Add disk image data to string repr ([`2d5b3ef`](https://github.com/swysocki/gpt-image/commit/2d5b3ef7e64705c97f74622b98636b21fdc0de3c))

## v0.6.1 (2022-07-24)
### Fix
* Return friendly partition attribute flags ([`6fb826f`](https://github.com/swysocki/gpt-image/commit/6fb826f715d74792fae265afe2634349989a0025))

## v0.6.0 (2022-07-23)
### Feature
* Add JSON output of objects ([`467f104`](https://github.com/swysocki/gpt-image/commit/467f1046c7898e878a03cb8f4ee8b8cf337b0c87))

## v0.5.0 (2022-07-14)
### Feature
* Migrate to struct module ([`aaa777f`](https://github.com/swysocki/gpt-image/commit/aaa777f2ab67c8d57c94dcbb3697ed3384a7a251))

## v0.4.2 (2022-07-12)
### Fix
* Allow setting the partition attribute on init ([`523e220`](https://github.com/swysocki/gpt-image/commit/523e220c3bc3023e3f59c76517f2338773d31645))
* Import modules in package namespace ([`c35476f`](https://github.com/swysocki/gpt-image/commit/c35476faa64b9af870648f0f1dd86e032a36040e))

## v0.4.1 (2022-07-09)
### Fix
* Use EFI spec mnemonics for attribute names ([`0e62e24`](https://github.com/swysocki/gpt-image/commit/0e62e24c1d80939068c7d4fd8c5dc703fbd99eb9))

## v0.4.0 (2022-05-28)
### Feature
* Allow setting partition attributes ([`fa73bde`](https://github.com/swysocki/gpt-image/commit/fa73bde27921561382613e6ed7ed1df88eb85458))

## v0.3.2 (2022-05-21)
### Fix
* Custom partition error class ([`bf2cdaa`](https://github.com/swysocki/gpt-image/commit/bf2cdaa514c8a1ff44d7df7c2e22d09ab4e9c1a1))
* Add missing types ([`f348697`](https://github.com/swysocki/gpt-image/commit/f348697dd7300a12e60d761874819f32b720eb0c))

## v0.3.1 (2022-05-08)
### Fix
* Allow guid to be None or UUID type ([`c2f15c7`](https://github.com/swysocki/gpt-image/commit/c2f15c7c12ca5a66023af8b9fcf5db241f2d70aa))
* Add marshal function ([`a7e06fd`](https://github.com/swysocki/gpt-image/commit/a7e06fd4fd80b0c8717da9803250d5eeb46969db))

## v0.3.0 (2022-05-07)
### Feature
* Read existing disk ([#14](https://github.com/swysocki/gpt-image/issues/14)) ([`ed83cb0`](https://github.com/swysocki/gpt-image/commit/ed83cb06efcdcdad2eee6be6930c8027565823b0))

## v0.2.2 (2022-04-03)
### Fix
* Adjust pmbr partition size ([#13](https://github.com/swysocki/gpt-image/issues/13)) ([`379d615`](https://github.com/swysocki/gpt-image/commit/379d615093451783643a7ec665c98f12ff907927))

## v0.2.1 (2022-02-27)
### Fix
* Add partition tests ([#9](https://github.com/swysocki/gpt-image/issues/9)) ([`da41ad2`](https://github.com/swysocki/gpt-image/commit/da41ad271ea56a2c0bfb53937ddac4f40599509f))

## v0.2.0 (2022-02-26)
### Feature
* Add semantic release ([#10](https://github.com/swysocki/gpt-image/issues/10)) ([`95177b2`](https://github.com/swysocki/gpt-image/commit/95177b21d1d45cb8bde0b736e332fb6452d3ddae))

### Fix
* Set version ([`a4262c1`](https://github.com/swysocki/gpt-image/commit/a4262c100acd4cbdf9f04177700a650710c8a757))
* Use setup.py for package version ([`3d69f94`](https://github.com/swysocki/gpt-image/commit/3d69f945fb22286ba6623e87f607ddb6c5dd7990))
* Remove partition wrapper ([`1f491ad`](https://github.com/swysocki/gpt-image/commit/1f491ad72c05c56094c7ea84b0888d34ffd3a546))
* Move logic to Disk object ([`4ab2211`](https://github.com/swysocki/gpt-image/commit/4ab2211a55beb23ce0f148a1a52387efe11fbd9d))

### Documentation
* Update comments ([`73e7052`](https://github.com/swysocki/gpt-image/commit/73e705213b4fb1144bb8ce92c6d895e7e7be6d4a))

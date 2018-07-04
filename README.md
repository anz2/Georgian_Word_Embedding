# Georgian_Word_Embedding
ქართული ნატურალური ენის დამუშავება და სიტვების ვექტორებად წარმოდგენა.

## Conda-ს დაყენება
'Anaconda 3' ვერსია არის საჭირო.
ამ მისამართიდან შეიძლება მისი გადმოწერა: 'https://www.anaconda.com/download/#linux'

## გარემოს დაყენება
გარემოს დაყენებისას 'conda_env/environment.yml' ფაილში შესაცვლელი იქნება ბოლო სტრიქონი
სადაც წერია გარემოს დაყენებისთვის საჭირო მისამართი:
...
prefix: /home/<username>/anaconda3/envs/gerogian_word_embedding
...
აქ <username> უნდა ჩაანაცვლოთ თქვენი მომხმარებლის სახელით linux-სისტემაში.

გარემოს შექმნით ამგვარად:
cd conda_env
conda env create -f environment.yml

გარემოს გააქტიურება:
source activate georgian_word_embedding
გარემოს დეაქტივაცია:
source deactivate

## მონაცემების გაფიტვრა არასასურველი სიმბოლოებისგან. მისი წინადადებებად და სიტყვებად დაყოფა.
გვაქვს რამდენიმე მუშაობის რეჟიმი:
- ერთი ფაილის სრული ტოკენიზაცია
  python text_to_sentence_split.py -ifp <input file path> -ofp <output file path> -ds
- დირექტორიაში ყველა ფაილების სრული ტოკენიზაცია და გაერთიანებული ტექსტური ფაილის შექმნაც (დატრენინგებისთვის საჭიროა)
  python text_to_sentence_split.py -ifd <input file directory path> -ofd <output file directory path> -ds -co
- დირექტორიაში ყველა ფაილების სრული ტოკენიზაცია და გაერთიანებული ტექსტური ფაილის შექმნაც (დატრენინგებისთვის საჭიროა)
  python text_to_sentence_split.py -ifd <input file directory path> -ofd <output file directory path> -ds -co
- მხოლოდ ტექსტური ფაილების გაერთიანება ერთ დიდ ტექსტურ ფაილში
  python text_to_sentence_split.py -ifd <input file directory path> -co -cofp <concatenated output file path>

სწრაფი ინსტრუქციების ნახვა შეიძლება help-ის გამოყენებით:
python text_to_sentence_split.py --help

მისი ყველა არსებული პარამეტრები:
- - ifp შემავალი ფაილის სრული ან მიმართებითი მისამართი
- - ofp გამომავალი ფაილის სრული ან მიმართებითი მისამართი
- - ifd შემავალი ფაილების შემცველი დირექტორიის სრული ან მიმართებითი მისამართი
- - ofd გამომავალი ფაილების შემცველი დირექტორიის სრული ან მიმართებითი მისამართი
- - msl მინიმალური წინადადების ზომა (სიმბოლოების რაოდენობა) რომელიც იქნება დაყოფილი სატრენინგოდ
- - co გამომავალი ყველა ტექსტური ფაილის ერთ ფაილში გაერთიანება (სატრენინგოდ გამოდგება მხოლოდ გაერთიანებული ფაილი)
- - ds წინადადებების დაყოფის განხორციელება (იმისათვის რომ სტკრიპტი გამოყენებული იქნას მხოლოდ ტექსტების გაერთიანებისთვისაც)
- - cofp გაერთიანებული ტექსტური ფაილის სრული ან მიმართებითი მისამართი

## fasttext დაყენება
https://github.com/facebookresearch/fastText
მოდელის დატრენინგება მოხდება შემდეგი ბრძანებით:
> ./fasttext skipgram -input data.txt -output model

## word2vec მოდელის დატრენინგება/გატესტვა შეიძლება შემდეგი ფაილებიდან
notebooks/testing_word2vec_gensim.ipynb
notebooks/training_word2vec_gensim.ipynb

მათი გაშვება შეიძლება უკვე დაყენებული conda-ს გარემოდან ამგვარად:
source activate georgian_word_embedding
jupyter notebook

## დატრენინგებული მოდელების გამოყენება:
დატრენინგებული მოდელების გადმოწერა შეიძლება შემდეგი მისამართიდან:
მოდელების გამოყენება ხდება using_models.py გაშვების შედეგად. იგი მუშაობს ინტერაქტიულ რეჟიმში 
და გადაცემულ ტექსტისთვის აბრუნებს შესაბამის პასუხს:
გვაქვს მოდელების შედარების რეჟიმი და ცალკ-ცალკე გაშვების რეჟიმი.
- ცალკე გაშვება:
python using_models.py <operation> -m <model name> -mp <model path>
აქ <operation>-ში შეიძლება დაიწეროს:
- -wanl ანალოგიების ამოცნობა. მაგ: 'კაცი ქალი ბიჭი' გადაცემის შედეგად უნდა დააბრუნოს 'გოგო' დიდი ალბათობით 
- -msw მსგავსი სიტყვები. მაგ: 'საქართველო'  გადაცემის შედეგად დააბრუნებს სხვადასხვა ქვეყნების სახელებს
- -ooo ზედმეტის გამოცნობა. მაგ: 'ძაღლი კატა თაგვი ბეღურა' გადაცემის შედეგად უნდა დააბრუნოს დიდი ალბათობით 'ბეღურა'
- შედარების რეჟიმით გაშვება: (ამ შემთხვევაში default მისამართები მაქვს აღებული მოდელებზე ამიტომ მათი მისამართები არ გადაეცება)
python using_models.py <operation> -cmp
აქ <operation>-ში შეიძლება დაიწეროს იგივე რაც ზემოთ ვახსენეთ. უბრალოდ ორივე მოდელის პასუხები დაიბეჭდება.

სწრაფი ინსტრუქციების ნახვა შეიძლება help-ის გამოყენებით:
python using_models.py --help

მისი ყველა არსებული პარამეტრები:
- -m მოდელის სახელი (fasttext, word2vec)
- -mp მოდელის სრული ანი მიმართებითი მისამართი
- -k საუკეთესო K ვარიანტის ჩვენება. მაგ: -msw ოპერაციისას 10 მსგავსი სიტყვის ჩვენება მოხდება -k 10 გამოყენებით
- -cmp მოდელების შედარების რეჟიმი
- -wanl ანალოგიების ამოცნობა. მაგ: 'კაცი ქალი ბიჭი' გადაცემის შედეგად უნდა დააბრუნოს 'გოგო' დიდი ალბათობით 
- -msw მსგავსი სიტყვები. მაგ: 'საქართველო'  გადაცემის შედეგად დააბრუნებს სხვადასხვა ქვეყნების სახელებს
- -ooo ზედმეტის გამოცნობა. მაგ: 'ძაღლი კატა თაგვი ბეღურა' გადაცემის შედეგად უნდა დააბრუნოს დიდი ალბათობით 'ბეღურა'
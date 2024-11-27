from django.shortcuts import render
from django.views.generic import TemplateView


# класс-представление
class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Главная"
        context["content"] = "Магазин телефонов DialStore"
        return context


# контроллер-функция (представление)
# def index(request):
#     context = {
#         'title': 'Home - Главная',
#         'content': 'Магазин мебели HOME',
#     }

#     return render(request, 'main/index.html', context)


class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - О нас"
        context["content"] = "О нас"
        context["text_on_page"] = """
    <div style="text-align: justify; padding-bottom: 1em;">
        <p style="margin-top: 1em;"><strong>DialStore</strong> — это больше, чем просто магазин телефонов. Наше название говорит само за себя: &laquo;Dial&raquo; напоминает о моменте связи, когда вы набираете номер, открывая новые горизонты общения. Мы предлагаем широкий выбор современных смартфонов, аксессуаров и гаджетов для связи, работы и развлечений.</p>
        <p style="margin-top: 1em;">Нас легко найти: мы расположены в торговом центре 
        <a href="https://galleria-minsk.by/" target="_blank" style="text-decoration: none; color: #007BFF;">&laquo;Галерея&raquo;</a> 
        в самом сердце Минска, на втором этаже. Здесь вы найдете уютный уголок технологий, где всегда готовы помочь с выбором.</p>
        <p style="margin-top: 1em; margin-bottom: 1em;">Загляните к нам, чтобы подобрать устройство, которое подчеркнет ваш стиль и сделает каждый день комфортнее. 
        <strong>DialStore</strong> — ваш ключ к миру современных технологий!</p>
    </div>
"""
        return context


class DeliveryPaymentView(TemplateView):
    template_name = "main/delivery_payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Доставка и оплата"
        context["content"] = "Доставка и оплата"
        context["text_on_page"] = """
    <div style="text-align: justify; padding-bottom: 1em;">
        <p style="margin-top: 1em;">В <strong>DialStore</strong> мы предлагаем удобные способы доставки и оплаты, чтобы сделать процесс покупки максимально комфортным для вас.</p>
        <h5 style="margin-top: 1em;">Доставка:</h5>
        <p>Мы осуществляем доставку по Минску и в регионы Беларуси. Доставка по Минску занимает 1-2 рабочих дня, а в регионы — до 5 рабочих дней.</p>
        <h5 style="margin-top: 1em;">Оплата:</h5>
        <p>Оплатить покупку можно несколькими способами: наличными при получении, банковской картой онлайн или через мобильные платежные системы.</p>
        <p style="margin-top: 1em;">Ваш комфорт и уверенность в каждой сделке — наш приоритет. Обращайтесь, и мы сделаем ваш процесс покупки максимально удобным!</p>
    </div>
"""
        return context
    

class ContactInfoView(TemplateView):
    template_name = "main/contact_info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Контактная информация"
        context["content"] = "Контактная информация"
        context["text_on_page"] = """
    <div style="text-align: justify; padding-bottom: 1em;">
        <p style="margin-top: 1em;">Если у вас есть вопросы или вам нужна консультация по выбору телефона, не стесняйтесь обращаться к нам!</p>
        <h5 style="margin-top: 1em;">Наши контакты:</h5>
        <p><strong>Адрес:</strong> Минск, ТЦ <a href="https://galleria-minsk.by/" target="_blank" style="text-decoration: none; color: #007BFF;">«Галерея»</a>, 2 этаж.</p>
        <p><strong>Телефон:</strong> +375 (29) 123-45-67</p>
        <p><strong>Email:</strong> support@dialstore.by</p>
        <h5 style="margin-top: 1em;">Часы работы:</h5>
        <p>Пн-Пт: с 10:00 до 20:00<br>Сб-Вс: с 11:00 до 18:00</p>
        <p style="margin-top: 1em;">Мы всегда рады помочь вам найти идеальный телефон или аксессуар! Звоните или приходите, и мы сделаем все, чтобы ваше общение с нами было комфортным и приятным.</p>
    </div>
"""
        return context


# def about(request):
#     context = {
#         'title': 'Home - О нас',
#         'content': 'О нас',
#         'text_on_page': 'Текст о том почему этот магазин такой классный, и какой хороший товар'
#     }

#     return render(request, 'main/about.html', context)

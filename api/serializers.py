from rest_framework import serializers
from .models import Balance, Expenditure, Transaction,Income,Debt,Wishlist



class BalanceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Balance
        fields = '__all__'
        read_only_fields = ('user',)

    def validate_amount(self, value):
        if value < -10000:
            raise serializers.ValidationError("Balance has hit the debt ceiling")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Expenditure
        fields = '__all__'
        read_only_fields = ('user',)
    
    def validate_amount(self, value):
        # if value < 0:
        #     raise serializers.ValidationError("Amount cannot be negative.")
        if value <= 10:
            raise serializers.ValidationError("Amount has to be more than 10")
        elif value >= 1000000:
            raise serializers.ValidationError("Max cap reached")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class IncomeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Income
        fields = '__all__'
        read_only_fields = ('user',)
    
    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative.")
        elif value <500 :
            raise serializers.ValidationError("Amount has to be more than 500")
        elif value >1000000 :
            raise serializers.ValidationError("Max Amount Cap Reached")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DebtSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Debt
        fields = '__all__'
        read_only_fields = ('user',)

    def validate_amount(self, value):
        if value<500.00:
            raise serializers.ValidationError("Amount has to be more than 500.")
        elif value > 1000000:
            raise serializers.ValidationError("Max Amount Cap Reached.")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Wishlist
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


from django.contrib.auth import get_user_model

User = get_user_model()

class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.filter(is_active=True))
    receiver = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.filter(is_active=True))

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('sender',)
    
    def validate_amount(self, value):
        if value > 150000:
            raise serializers.ValidationError("Amount cannnot exceed 150,000")
        elif value <500 :
            raise serializers.ValidationError("Amount has to be more than 500")
        return value

    def create(self, validated_data):
        sender_username = validated_data.pop('sender')
        receiver_username = validated_data.pop('receiver')

        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)

        transaction = Transaction.objects.create(sender=sender, receiver=receiver, **validated_data)
        return transaction
